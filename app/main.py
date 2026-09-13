from fastapi import FastAPI
from sqlalchemy import text
from app.api.ai import router as ai_router
from app.api.approval import router as approval_router
from app.api.customer import router as customer_router
from app.api.invoice import router as invoice_router
from app.api.payment import router as payment_router
from app.api.subscription import router as subscription_router
from app.api.ticket import router as ticket_router
from app.core.config import settings
from app.db.session import engine
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered customer support and billing assistant with function calling",
)
app.include_router(customer_router, prefix="/api/v1")
app.include_router(invoice_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")
app.include_router(subscription_router, prefix="/api/v1")
app.include_router(ticket_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")
app.include_router(approval_router, prefix="/api/v1")
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