from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.subscription import Subscription
def create_subscription(
    db: Session,
    customer_id: int,
    plan_name: str,
    status: str,
    expires_at,
) -> Subscription:
    subscription = Subscription(
        customer_id=customer_id,
        plan_name=plan_name,
        status=status,
        expires_at=expires_at,
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription
def get_subscription_by_id(
    db: Session,
    subscription_id: int,
) -> Subscription | None:
    statement = select(Subscription).where(
        Subscription.id == subscription_id
    )
    return db.scalar(statement)