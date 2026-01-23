from fastapi import FastAPI
from app.api.routes import router as route_router
from app.db.base import Base
from app.db.session import engine

# Create all tables (for local/dev only)
# In production use Alembic migrations
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Planned vs Actual Route Analysis API",
    description="Last-mile logistics route comparison service",
    version="1.0.0"
)

# Register routers
app.include_router(
    route_router,
    prefix="/api/v1",
    tags=["Routes"]
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
