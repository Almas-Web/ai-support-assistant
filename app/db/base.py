from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.models import (
    Customer,
    Invoice,
    Payment,
    Subscription,
    SupportTicket,
)