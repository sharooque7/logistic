from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class RouteMetric(Base):
    __tablename__ = "route_metrics"

    id = Column(Integer, primary_key=True)

    route_id = Column(
        String(50),
        ForeignKey("routes.route_id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )

    total_planned_distance_km = Column(Float)
    total_actual_distance_km = Column(Float)

    distance_delta_km = Column(Float)
    distance_delta_percent = Column(Float)

    order_matched_stops = Column(Integer)
    order_match_percentage = Column(Float)

    prefix_match_count = Column(Integer)

    total_stops = Column(Integer)

    generated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relationship
    route = relationship("Route", backref="metrics")

    __table_args__ = (
        UniqueConstraint("route_id", name="unique_route_metrics"),
    )
