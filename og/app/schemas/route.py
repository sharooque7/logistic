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
        orm_mode = True
        from_attributes = True  

