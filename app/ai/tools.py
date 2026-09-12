from sqlalchemy.orm import Session
from app.services.customer_service import get_customer_by_id
from app.services.invoice_service import get_invoice_by_id
from app.services.payment_service import get_payment_by_id
from app.services.subscription_service import get_subscription_by_id
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
def get_payment_status(
    db: Session,
    payment_id: int,
) -> dict:
    payment = get_payment_by_id(
        db=db,
        payment_id=payment_id,
    )
    if payment is None:
        return {
            "success": False,
            "error": "Payment not found",
            "payment_id": payment_id,
        }
    return {
        "success": True,
        "payment": {
            "id": payment.id,
            "customer_id": payment.customer_id,
            "invoice_id": payment.invoice_id,
            "amount": float(payment.amount),
            "status": payment.status,
            "payment_method": payment.payment_method,
            "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
        },
    }
def get_subscription(
    db: Session,
    subscription_id: int,
) -> dict:
    subscription = get_subscription_by_id(
        db=db,
        subscription_id=subscription_id,
    )
    if subscription is None:
        return {
            "success": False,
            "error": "Subscription not found",
            "subscription_id": subscription_id,
        }
    return {
        "success": True,
        "subscription": {
            "id": subscription.id,
            "customer_id": subscription.customer_id,
            "plan_name": subscription.plan_name,
            "status": subscription.status,
            "started_at": subscription.started_at.isoformat(),
            "expires_at": (
                subscription.expires_at.isoformat()
                if subscription.expires_at
                else None
            ),
        },
    }