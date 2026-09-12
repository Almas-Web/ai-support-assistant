from datetime import datetime
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.services.ticket_service import create_ticket


router = APIRouter(
    prefix="/tickets",
    tags=["Support Tickets"],
)


class TicketCreate(BaseModel):
    customer_id: int
    subject: str
    description: str
    priority: str = "medium"


class TicketResponse(BaseModel):
    id: int
    customer_id: int
    subject: str
    description: str
    status: str
    priority: str
    created_at: datetime


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket_api(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
):
    return create_ticket(
        db=db,
        customer_id=ticket_data.customer_id,
        subject=ticket_data.subject,
        description=ticket_data.description,
        priority=ticket_data.priority,
    )