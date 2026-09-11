from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        nullable=False,
    )

    invoices = relationship(
        "Invoice",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    payments = relationship(
        "Payment",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    subscriptions = relationship(
        "Subscription",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    tickets = relationship(
        "SupportTicket",
        back_populates="customer",
        cascade="all, delete-orphan",
    )