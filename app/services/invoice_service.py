from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.invoice import Invoice


def create_invoice(
    db: Session,
    customer_id: int,
    amount: float,
    status: str,
    due_at,
) -> Invoice:
    invoice = Invoice(
        customer_id=customer_id,
        amount=amount,
        status=status,
        due_at=due_at,
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return invoice


def get_invoice_by_id(
    db: Session,
    invoice_id: int,
) -> Invoice | None:
    statement = select(Invoice).where(
        Invoice.id == invoice_id
    )

    return db.scalar(statement)