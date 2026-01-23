from sqlalchemy import Column, String, Date, Time, Numeric, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Route(Base):
    __tablename__ = "routes"

    route_id = Column(String(50), primary_key=True)
    station_code = Column(String(10))
    date_YYYY_MM_DD = Column("date_yyyy_mm_dd", Date)
    departure_time_utc = Column(Time)
    executor_capacity_cm3 = Column(Numeric(10, 2))
    route_score = Column(String(10))
    created_at = Column(TIMESTAMP, server_default=func.now())

    stops = relationship("Stop", back_populates="route", cascade="all, delete")
    actual_sequence = relationship("ActualRouteSequence", back_populates="route", cascade="all, delete")
