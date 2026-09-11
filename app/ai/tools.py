from sqlalchemy.orm import Session

from app.services.customer_service import get_customer_by_id

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