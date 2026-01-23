import math

from app.models import stops

station = None
dropoffs = []

def seperate_station_and_dropoffs(stops):
    station = None
    dropoffs = []
    for stop in stops:
        print(stop)
        if stop["type"].lower() == "station":
            station = stop
        else:
            dropoffs.append(stop)

    if not station:
        raise ValueError("No station found")

    return station, dropoffs

def haversine(lat1, lon1, lat2, lon2):
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


def generate_planned_route(route, stops):
    station, dropoffs = seperate_station_and_dropoffs(stops)
    planned_route = []
    current = station
    remaining = dropoffs.copy()
    sequence = 1

    while remaining:
        nearest = min(
            remaining,
            key=lambda stop: haversine(
                current["lat"],
                current["lng"],
                stop["lat"],
                stop["lng"],
            ),
        )

        planned_route.append({
            "stop_code": nearest["stop_code"],
            "planned_sequence": sequence,
            "lat": nearest["lat"],
            "lng": nearest["lng"],
            "zone_id": nearest["zone_id"],
        })

        sequence += 1
        remaining.remove(nearest)
        current = nearest

    planned_route.insert(0, station)

    return route, planned_route


def total_route_distance(stops):
    total = 0.0

    for i in range(len(stops) - 1):
        s1 = stops[i]
        s2 = stops[i + 1]

        total += haversine(
            s1["lat"], s1["lng"],
            s2["lat"], s2["lng"]
        )

    return round(total, 2)

def order_match_percentage(planned, actual):
    matches = 0
    length = min(len(planned), len(actual))

    for i in range(length):
        if planned[i]["stop_code"] == actual[i]["stop_code"]:
            matches += 1
    
    print(matches, length)

    return round((matches / length) * 100, 2)

def prefix_match_percentage(planned, actual):
    matches = 0
    length = min(len(planned), len(actual))

    for i in range(length):
        if planned[i]["stop_code"][0] == actual[i]["stop_code"][0]:
            matches += 1
        else:
            break
    
    print(matches, length)

    return round((matches / length) * 100, 2)