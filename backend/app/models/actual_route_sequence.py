from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class ActualRouteSequence(Base):
    __tablename__ = "actual_route_sequence"

    id = Column(Integer, primary_key=True)
    route_id = Column(String(50), ForeignKey("routes.route_id", ondelete="CASCADE"))
    stop_code = Column(String(10), nullable=False)
    actual_sequence = Column(Integer, nullable=False)
    recorded_at = Column(TIMESTAMP, server_default=func.now())

    route = relationship("Route", back_populates="actual_sequence")
