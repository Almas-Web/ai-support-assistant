from datetime import datetime
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.services.subscription_service import create_subscription
router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"],
)
class SubscriptionCreate(BaseModel):
    customer_id: int
    plan_name: str
    status: str
    expires_at: datetime | None = None
class SubscriptionResponse(BaseModel):
    id: int
    customer_id: int
    plan_name: str
    status: str
    started_at: datetime
    expires_at: datetime | None
@router.post(
    "",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_subscription_api(
    subscription_data: SubscriptionCreate,
    db: Session = Depends(get_db),
):
    return create_subscription(
        db=db,
        customer_id=subscription_data.customer_id,
        plan_name=subscription_data.plan_name,
        status=subscription_data.status,
        expires_at=subscription_data.expires_at,
    )