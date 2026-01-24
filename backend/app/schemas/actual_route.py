from pydantic import BaseModel

class ActualStopResponse(BaseModel):
    stop_code: str
    actual_sequence: int

    class Config:
        from_attributes = True  
    
