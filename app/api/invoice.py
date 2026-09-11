from datetime import datetime

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.invoice_service import create_invoice


router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"],
)


class InvoiceCreate(BaseModel):
    customer_id: int
    amount: float
    status: str
    due_at: datetime


class InvoiceResponse(BaseModel):
    id: int
    customer_id: int
    amount: float
    status: str
    issued_at: datetime
    due_at: datetime


@router.post(
    "",
    response_model=InvoiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_invoice_api(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db),
):
    return create_invoice(
        db=db,
        customer_id=invoice_data.customer_id,
        amount=invoice_data.amount,
        status=invoice_data.status,
        due_at=invoice_data.due_at,
    )