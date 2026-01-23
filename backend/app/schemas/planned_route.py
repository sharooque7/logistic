from pydantic import BaseModel
from typing import List
from app.schemas.route import RouteResponse


class PlannedStopResponse(BaseModel):
    stop_code: str
    planned_sequence: int
    lat: float
    lng: float
    zone_id: str | None
    type: str


class PlannedRouteResponse(BaseModel):
    route: RouteResponse
    planned_route: List[PlannedStopResponse]

    class Config:
        from_attributes = True
