from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.ticket import SupportTicket


def create_ticket(
    db: Session,
    customer_id: int,
    subject: str,
    description: str,
    priority: str,
) -> SupportTicket:
    ticket = SupportTicket(
        customer_id=customer_id,
        subject=subject,
        description=description,
        priority=priority,
        status="open",
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def get_ticket_by_id(
    db: Session,
    ticket_id: int,
) -> SupportTicket | None:
    statement = select(SupportTicket).where(
        SupportTicket.id == ticket_id
    )
    return db.scalar(statement)