from typing import List
from fastapi import Query
from app.db.session import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.repositories.route_repository import (
    get_all_routes,
    get_all_routes_paginated,
    get_route,
    get_route_stops,
    get_actual_route_sequence,
    get_actual_route,
    get_route_with_stops,
    save_planned_route,
    get_planned_route,
    save_route_metrics,
    get_route_metric,
    get_total_routes_total_stops
)
from app.schemas.stop import StopResponse
from app.schemas.route import RouteResponse, RouteResponseWithStopsCount,RouteResponseWithRouteAndStopCount
from app.schemas.actual_route import ActualStopResponse
from app.schemas.planned_route import PlannedRouteResponse
from app.services.router_planner import RoutePlanner
from app.schemas.route_metric import RouteMetricBase,RouteMetricRepsonse

router = APIRouter(prefix="/routes", tags=["Routes"])

@router.get("/all", response_model=List[RouteResponseWithStopsCount])
def fetch_routes(db: Session = Depends(get_db)):
    return get_all_routes(db)

@router.get("/total_routes_and_stops", response_model=RouteResponseWithRouteAndStopCount)
def fetch_routes(db: Session = Depends(get_db)):
    return get_total_routes_total_stops(db)
   
@router.get("", response_model=List[RouteResponseWithStopsCount])
def fetch_routes(
    skip: int = Query(0, ge=0),      
    limit: int = Query(10, ge=1, le=100), 
    db: Session = Depends(get_db)
):
    return get_all_routes_paginated(db, skip=skip, limit=limit)

@router.get("/{route_id}", response_model=RouteResponse)
def fetch_route(route_id: str, db: Session = Depends(get_db)):
    route = get_route(db, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.get("/{route_id}/stops", response_model=List[StopResponse])
def fetch_route_stops(route_id: str, db: Session = Depends(get_db)):
    return get_route_stops(db, route_id)

@router.get("/{route_id}/actual", response_model=List[ActualStopResponse])
def fetch_actual_route(route_id: str, db: Session = Depends(get_db)):
    return get_actual_route_sequence(db, route_id)

@router.post("/{route_id}/generate/planned_routes", response_model=PlannedRouteResponse)
def generate_planned_routes(route_id: str, db: Session = Depends(get_db)):
    route = get_route(db, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    stops = get_route_stops(db, route_id)
    if not stops:
        raise HTTPException(status_code=404, detail="No stops found for the given route")
    
    planner = RoutePlanner(route, stops)
    planned_route = planner.generate_planned_route()

    save_planned_route(db, route_id, planned_route)

    return {
        "route": route,
        "planned_route": planned_route,
    }

@router.get("/{route_id}/comparison")
def get_route_comparison(route_id: str, db: Session = Depends(get_db)):
    route = get_route(db, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    planned_route = get_planned_route(db, route_id)
    actual_route = get_actual_route(db, route_id)

    planned_km = RoutePlanner.total_route_distance(planned_route)
    actual_km = RoutePlanner.total_route_distance(actual_route)
    order_matches, order_match_percentage = RoutePlanner.order_match_percentage(planned_route, actual_route)
    prefix_matches = RoutePlanner.prefix_match_count(planned_route, actual_route)

    metric = {
        "total_planned_distance_km": planned_km,
        "total_actual_distance_km": actual_km,
        "distance_delta_km": round(planned_km - actual_km if planned_km is not None and actual_km is not None else 0, 2),
        "distance_delta_percent": round(((planned_km - actual_km) / actual_km * 100) if actual_km and actual_km != 0 else 0,2),
        "order_matched_stops": order_matches,
        "order_match_percentage": order_match_percentage,
        "prefix_match_count": prefix_matches,
        "total_stops": len(planned_route),
    }

    save_route_metrics(db, route_id, metric)

    return {
        "route": {
            "route_id": route.route_id,
            "station_code": route.station_code,
            "date_YYYY_MM_DD": route.date_YYYY_MM_DD,
            "departure_time_utc": route.departure_time_utc,
            "executor_capacity_cm3": float(route.executor_capacity_cm3),
            "route_score": route.route_score,
        },
        "planned_route": planned_route,
        "actual_route": actual_route,
    }


@router.get("/{route_id}/metrics", response_model=RouteMetricRepsonse)
def fetch_route_metric(route_id: str, db: Session = Depends(get_db)):
    route = get_route(db, route_id)
    if not route:
        raise HTTPException(
            status_code=404,
            detail="Route not found"
        )
    
    metric = get_route_metric(db, route_id)

    if not metric:
        raise HTTPException(
            status_code=404,
            detail="Route metrics not found"
        )
    
    return {
        "route": route,
        "metrics": metric
    }
