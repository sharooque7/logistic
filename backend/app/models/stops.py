from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Stop(Base):
    __tablename__ = "stops"

    stop_id = Column(Integer, primary_key=True)
    route_id = Column(String(50), ForeignKey("routes.route_id", ondelete="CASCADE"))
    stop_code = Column(String(10))
    lat = Column(Numeric(9, 6))
    lng = Column(Numeric(9, 6))
    type = Column(String(20))
    zone_id = Column(String(20))

    route = relationship("Route", back_populates="stops")
