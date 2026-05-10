from datetime import date, datetime

from sqlalchemy import Date, DateTime, Index, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base, TimestampMixin


class SignalEvent(Base, TimestampMixin):
    __tablename__ = "signal_events"
    __table_args__ = (Index("ix_signal_events_trade_date_symbol", "trade_date", "symbol"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    event_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    trade_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    symbol: Mapped[str | None] = mapped_column(String(16), nullable=True, index=True)
    signal_type: Mapped[str] = mapped_column(String(32), nullable=False)
    source_module: Mapped[str] = mapped_column(String(64), nullable=False)
    rule_version: Mapped[str] = mapped_column(String(32), nullable=False)
    score_snapshot: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    risk_snapshot: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    decision: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
