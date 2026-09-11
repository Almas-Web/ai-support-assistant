from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id"),
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
    payment_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    paid_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    customer = relationship(
        "Customer",
        back_populates="payments",
    )

    invoice = relationship(
        "Invoice",
        back_populates="payments",
    )