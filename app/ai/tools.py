from sqlalchemy.orm import Session

from app.services.customer_service import get_customer_by_id
from app.services.invoice_service import get_invoice_by_id


def get_customer(
    db: Session,
    customer_id: int,
) -> dict:
    customer = get_customer_by_id(
        db=db,
        customer_id=customer_id,
    )

    if customer is None:
        return {
            "success": False,
            "error": "Customer not found",
            "customer_id": customer_id,
        }

    return {
        "success": True,
        "customer": {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "created_at": customer.created_at.isoformat(),
        },
    }


def get_invoice(
    db: Session,
    invoice_id: int,
) -> dict:
    invoice = get_invoice_by_id(
        db=db,
        invoice_id=invoice_id,
    )

    if invoice is None:
        return {
            "success": False,
            "error": "Invoice not found",
            "invoice_id": invoice_id,
        }

    return {
        "success": True,
        "invoice": {
            "id": invoice.id,
            "customer_id": invoice.customer_id,
            "amount": float(invoice.amount),
            "status": invoice.status,
            "issued_at": invoice.issued_at.isoformat(),
            "due_at": invoice.due_at.isoformat(),
        },
    }