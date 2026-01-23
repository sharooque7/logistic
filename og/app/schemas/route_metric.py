from pydantic import BaseModel

from app.schemas.route import RouteResponse


class RouteMetricBase(BaseModel):
    route_id: str

    total_planned_distance_km: float | None = None
    total_actual_distance_km: float | None = None

    distance_delta_km: float | None = None
    distance_delta_percent: float | None = None

    order_matched_stops: int | None = None
    order_match_percentage: float | None = None

    prefix_match_count: int | None = None
    total_stops: int | None = None

class RouteMetricRepsonse(BaseModel):
    route: RouteResponse
    metrics: RouteMetricBase
    
    class Config:
        from_attributes = True
