# app/models/planned_route_sequence.py

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class PlannedRouteSequence(Base):
    __tablename__ = "planned_route_sequence"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(String(50), ForeignKey("routes.route_id", ondelete="CASCADE"))
    stop_code = Column(String(10), nullable=False)
    planned_sequence = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
