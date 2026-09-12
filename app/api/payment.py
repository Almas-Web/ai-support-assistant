from datetime import datetime

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.payment_service import create_payment


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


class PaymentCreate(BaseModel):
    customer_id: int
    invoice_id: int
    amount: float
    status: str
    payment_method: str
    paid_at: datetime | None = None


class PaymentResponse(BaseModel):
    id: int
    customer_id: int
    invoice_id: int
    amount: float
    status: str
    payment_method: str
    paid_at: datetime | None


@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment_api(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
):
    return create_payment(
        db=db,
        customer_id=payment_data.customer_id,
        invoice_id=payment_data.invoice_id,
        amount=payment_data.amount,
        status=payment_data.status,
        payment_method=payment_data.payment_method,
        paid_at=payment_data.paid_at,
    )