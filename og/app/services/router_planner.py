import math
from typing import List, Tuple
from app.models.stops import Stop
from app.models.routes import Route


class RoutePlanner:
    def __init__(self, route: Route, stops: List[Stop]):
        self.route = route
        self.stops = stops
        self.station = None
        self.dropoffs = []

    # ----------------------------
    # Helpers
    # ----------------------------

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2) -> float:
        R = 6371  # Earth radius in KM

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    # ----------------------------
    # Core Logic
    # ----------------------------

    def seperate_station_and_dropoffs(self) -> Tuple[Stop, List[Stop]]:
        for stop in self.stops:
            if stop.type.lower() == "station":
                self.station = stop
            else:
                self.dropoffs.append(stop)

        if not self.station:
            raise ValueError("No station found in route")

        return self.station, self.dropoffs

    def generate_planned_route(self) -> List[dict]:
        station, dropoffs = self.seperate_station_and_dropoffs()

        planned_route = []
        current = station
        remaining = dropoffs.copy()
        sequence = 1

        while remaining:
            nearest = min(
                remaining,
                key=lambda stop: self.haversine(
                    current.lat,
                    current.lng,
                    stop.lat,
                    stop.lng,
                ),
            )

            planned_route.append({
                "stop_code": nearest.stop_code,
                "planned_sequence": sequence,
                "lat": nearest.lat,
                "lng": nearest.lng,
                "zone_id": nearest.zone_id,
                "type": nearest.type,
            })

            sequence += 1
            remaining.remove(nearest)
            current = nearest

        # Add station at the beginning
        planned_route.insert(0, {
            "stop_code": station.stop_code,
            "planned_sequence": 0,
            "lat": station.lat,
            "lng": station.lng,
            "zone_id": station.zone_id,
            "type": station.type,
        })

        return planned_route

    # ----------------------------
    # Metrics
    # ----------------------------

    @staticmethod
    def total_route_distance(stops: List[dict]) -> float:
        total = 0.0

        for i in range(len(stops) - 1):
            s1, s2 = stops[i], stops[i + 1]
            total += RoutePlanner.haversine(
                s1["lat"], s1["lng"],
                s2["lat"], s2["lng"]
            )

        return round(total, 2)

    @staticmethod
    def order_match_percentage(planned: List[dict], actual: List[dict]) -> float:
        matches = 0
        length = min(len(planned), len(actual))

        for i in range(length):
            if planned[i]["stop_code"] == actual[i]["stop_code"]:
                matches += 1

        return matches, round((matches / length) * 100, 2) if length else 0.0

    @staticmethod
    def prefix_match_count(planned: List[dict], actual: List[dict], cap: int = 10) -> int:
        matches = 0
        length = min(len(planned), len(actual), cap)

        for i in range(length):
            if planned[i]["stop_code"] == actual[i]["stop_code"]:
                matches += 1
            else:
                break

        return matches
