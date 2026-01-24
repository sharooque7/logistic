from typing import List
from sqlalchemy.sql import func
from app.models.stops import Stop
from sqlalchemy.orm import Session
from app.models.routes import Route
from sqlalchemy.dialects.postgresql import insert
from app.models.actual_route_sequence import ActualRouteSequence
from app.models.planned_route_sequence import PlannedRouteSequence
from sqlalchemy.dialects.postgresql import insert
from app.models.route_metric import RouteMetric



def get_all_routes(db: Session):
    # return db.query(Route).all()
    rows = (
        db.query(
            Route,
            func.count(Stop.stop_code).label("stop_count")
        )
        .outerjoin(Stop, Route.route_id == Stop.route_id)
        .group_by(Route.route_id)
        .all()
    )

    result = []
    for route, stop_count in rows:
        result.append({
            "route_id": route.route_id,
            "station_code": route.station_code,
            "date_YYYY_MM_DD": route.date_YYYY_MM_DD,
            "departure_time_utc": route.departure_time_utc,
            "executor_capacity_cm3": route.executor_capacity_cm3,
            "route_score": route.route_score,
            "stop_count": stop_count,
        })

    return result


def get_total_routes_total_stops(db: Session):
    result = (
        db.query(
            func.count(func.distinct(Route.route_id)).label("route_count"),
            func.count(Stop.route_id).label("stop_count"),
        )
        .outerjoin(Stop, Stop.route_id == Route.route_id)
        .one()
    )

    return {
        "route_count": result.route_count,
        "stop_count": result.stop_count,
    }




def get_all_routes_paginated(db: Session, skip: int = 0, limit: int = 10) -> List[Route]:
    # return db.query(Route).offset(skip).limit(limit).all()
    rows = (
            db.query(
                Route,
                func.count(Stop.stop_code).label("stop_count")
            )
            .outerjoin(Stop, Stop.route_id == Route.route_id)
            .group_by(Route.route_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    result = []
    for route, stop_count in rows:
        result.append({
            "route_id": route.route_id,
            "station_code": route.station_code,
            "date_YYYY_MM_DD": route.date_YYYY_MM_DD,
            "departure_time_utc": route.departure_time_utc,
            "executor_capacity_cm3": route.executor_capacity_cm3,
            "route_score": route.route_score,
            "stop_count": stop_count,
        })

    return result


def get_route(db: Session, route_id: str):
    return db.query(Route).filter(Route.route_id == route_id).first()

def get_route_stops(db: Session, route_id: str):
    return (
        db.query(Stop)
        .filter(Stop.route_id == route_id)
        .all()
    )

def get_actual_route_sequence(db: Session, route_id: str):
    return (
        db.query(ActualRouteSequence)
        .filter(ActualRouteSequence.route_id == route_id)
        .order_by(ActualRouteSequence.actual_sequence)
        .all()
    )

def get_route_with_stops(db: Session, route_id: str):
    route = db.query(Route).filter(Route.route_id == route_id).first()
    if not route:
        return None

    stops = db.query(Stop).filter(Stop.route_id == route_id).all()
    actual_stops = db.query(ActualRouteSequence).filter(ActualRouteSequence.route_id == route_id).all()

    return {
        "route": route,
        "stops": stops,
        "actual_stops": actual_stops
    }

def save_planned_route(db: Session, route_id: str, planned_route: list[dict]):
    records = [
        {
            "route_id": route_id,
            "stop_code": stop["stop_code"],
            "planned_sequence": stop["planned_sequence"],
        }
        for stop in planned_route
    ]

    stmt = insert(PlannedRouteSequence).values(records)

    stmt = stmt.on_conflict_do_nothing(
        index_elements=["route_id", "stop_code"]
    )

    db.execute(stmt)
    db.commit()

def get_planned_route(db: Session, route_id: str):
    rows = (
        db.query(
            PlannedRouteSequence.stop_code,
            PlannedRouteSequence.planned_sequence,
            Stop.lat,
            Stop.lng,
            Stop.zone_id,
            Stop.type,
        )
        .join(Stop, 
              (Stop.route_id == PlannedRouteSequence.route_id) &
              (Stop.stop_code == PlannedRouteSequence.stop_code)
        )
        .filter(PlannedRouteSequence.route_id == route_id)
        .order_by(PlannedRouteSequence.planned_sequence.asc())
        .all()
    )

    return [
        {
            "stop_code": r.stop_code,
            "planned_sequence": r.planned_sequence,
            "lat": r.lat,
            "lng": r.lng,
            "zone_id": r.zone_id,
            "type": r.type,
        }
        for r in rows
    ]

def get_actual_route(db: Session, route_id: str):
    rows = (
        db.query(
            ActualRouteSequence.stop_code,
            ActualRouteSequence.actual_sequence,
            Stop.lat,
            Stop.lng,
            Stop.zone_id,
            Stop.type,
        )
        .join(Stop,
              (Stop.route_id == ActualRouteSequence.route_id) &
              (Stop.stop_code == ActualRouteSequence.stop_code)
        )
        .filter(ActualRouteSequence.route_id == route_id)
        .order_by(ActualRouteSequence.actual_sequence.asc())
        .all()
    )

    return [
        {
            "stop_code": r.stop_code,
            "actual_sequence": r.actual_sequence,
            "lat": r.lat,
            "lng": r.lng,
            "zone_id": r.zone_id,
            "type": r.type,
        }
        for r in rows
    ]


def save_route_metrics(db: Session, route_id: str, metric: dict):
    stmt = insert(RouteMetric).values(
        route_id=route_id,
        **metric
    )

    stmt = stmt.on_conflict_do_update(
        index_elements=["route_id"],
        set_={
            "total_planned_distance_km": metric["total_planned_distance_km"],
            "total_actual_distance_km": metric["total_actual_distance_km"],
            "distance_delta_km": metric["distance_delta_km"],
            "distance_delta_percent": metric["distance_delta_percent"],
            "order_matched_stops": metric["order_matched_stops"],
            "order_match_percentage": metric["order_match_percentage"],
            "prefix_match_count": metric["prefix_match_count"],
            "total_stops": metric["total_stops"],
            "generated_at": func.now(),
        }
    )

    db.execute(stmt)
    db.commit()


def get_route_metric(db: Session, route_id: str):
    return (
        db.query(RouteMetric)
        .filter(RouteMetric.route_id == route_id)
        .first()
    )