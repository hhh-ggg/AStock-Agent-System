from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base, TimestampMixin


class ReviewDaily(Base, TimestampMixin):
    __tablename__ = "review_daily"

    id: Mapped[int] = mapped_column(primary_key=True)
    review_date: Mapped[date] = mapped_column(Date, unique=True, nullable=False)
    rule_version: Mapped[str] = mapped_column(String(32), nullable=False)
    total_signals: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    valid_signals: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    hit_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    miss_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_return_1d: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    avg_return_3d: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    avg_return_5d: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
