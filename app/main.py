from fastapi import FastAPI

from app.core.config import get_settings
from app.db.base import Base
from app.db.database import engine
from app.models import order
from app.routers import orders

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="API for validating and processing e-commerce orders.",
    version="1.0.0",
)

app.include_router(orders.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
