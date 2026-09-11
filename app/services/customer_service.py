from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


def create_customer(
    db: Session,
    customer_data: CustomerCreate,
) -> Customer:
    customer = Customer(
        name=customer_data.name,
        email=customer_data.email,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


def get_customers(db: Session) -> list[Customer]:
    statement = select(Customer).order_by(Customer.id)

    return list(db.scalars(statement).all())


def get_customer_by_id(
    db: Session,
    customer_id: int,
) -> Customer | None:
    statement = select(Customer).where(Customer.id == customer_id)

    return db.scalar(statement)