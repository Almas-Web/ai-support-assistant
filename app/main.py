from fastapi import FastAPI
from sqlalchemy import text

from app.api.customer import router as customer_router
from app.core.config import settings
from app.db.session import engine


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered customer support and billing assistant with function calling",
)


app.include_router(
    customer_router,
    prefix="/api/v1",
)


@app.get("/")
def health_check():
    return {
        "message": "AI Customer Support & Billing Assistant API is running",
        "version": settings.app_version,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/health/database")
def database_health():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }