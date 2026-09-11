from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )
    amount: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
    )
    issued_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        nullable=False,
    )
    due_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )

    customer = relationship(
        "Customer",
        back_populates="invoices",
    )

    payments = relationship(
        "Payment",
        back_populates="invoice",
        cascade="all, delete-orphan",
    )