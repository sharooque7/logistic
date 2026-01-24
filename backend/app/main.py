from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as route_router
from app.db.base import Base
from app.db.session import engine

# Create all tables (for local/dev only)
# In production use Alembic migrations
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="Planned vs Actual Route Analysis API",
    description="Last-mile logistics route comparison service",
    version="1.0.0"
)

# Allow CORS
origins = [
    "*",  # Vite frontend
    # add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(
    route_router,
    prefix="/api/v1",
    tags=["Routes"]
)

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}
