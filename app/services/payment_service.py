from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.payment import Payment


def create_payment(
    db: Session,
    customer_id: int,
    invoice_id: int,
    amount: float,
    status: str,
    payment_method: str,
    paid_at,
) -> Payment:
    payment = Payment(
        customer_id=customer_id,
        invoice_id=invoice_id,
        amount=amount,
        status=status,
        payment_method=payment_method,
        paid_at=paid_at,
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


def get_payment_by_id(
    db: Session,
    payment_id: int,
) -> Payment | None:
    statement = select(Payment).where(
        Payment.id == payment_id
    )

    return db.scalar(statement)