from datetime import date, time
from pydantic import BaseModel
from typing import List, Optional

class RouteResponse(BaseModel):
    route_id: str
    station_code: Optional[str]
    date_YYYY_MM_DD: date
    departure_time_utc: time
    executor_capacity_cm3: float
    route_score: str

    class Config:
        from_attributes = True  
        
class RouteResponseWithStopsCount(BaseModel):
    route_id: str
    station_code: Optional[str]
    date_YYYY_MM_DD: date
    departure_time_utc: time
    stop_count: int
    executor_capacity_cm3: float
    route_score: str

    class Config:
        from_attributes = True  
        
        
class RouteResponseWithRouteAndStopCount(BaseModel):
    stop_count: int
    route_count: int

    class Config:
        from_attributes = True  

