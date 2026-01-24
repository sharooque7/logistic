from pydantic import BaseModel

class StopResponse(BaseModel):
    stop_code: str
    lat: float
    lng: float
    type: str
    zone_id: str | None

    class Config:
        from_attributes = True  

