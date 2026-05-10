"""initial_core_tables

Revision ID: ff9dace0b390
Revises:
Create Date: 2026-05-11 00:32:33.166572

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ff9dace0b390"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "stocks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("symbol", sa.String(16), unique=True, nullable=False),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("exchange", sa.String(16), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_stocks_symbol", "stocks", ["symbol"])

    op.create_table(
        "daily_bars",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("symbol", sa.String(16), nullable=False),
        sa.Column("trade_date", sa.Date, nullable=False),
        sa.Column("open", sa.Numeric(12, 4), nullable=True),
        sa.Column("high", sa.Numeric(12, 4), nullable=True),
        sa.Column("low", sa.Numeric(12, 4), nullable=True),
        sa.Column("close", sa.Numeric(12, 4), nullable=True),
        sa.Column("volume", sa.Numeric(20, 2), nullable=True),
        sa.Column("amount", sa.Numeric(20, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("symbol", "trade_date"),
    )
    op.create_index("ix_daily_bars_symbol", "daily_bars", ["symbol"])
    op.create_index("ix_daily_bars_trade_date", "daily_bars", ["trade_date"])

    op.create_table(
        "positions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("symbol", sa.String(16), nullable=False),
        sa.Column("quantity", sa.Numeric(16, 2), nullable=False),
        sa.Column("avg_cost", sa.Numeric(12, 4), nullable=False),
        sa.Column("position_date", sa.Date, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_positions_symbol", "positions", ["symbol"])

    op.create_table(
        "signal_events",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("event_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("trade_date", sa.Date, nullable=False),
        sa.Column("symbol", sa.String(16), nullable=True),
        sa.Column("signal_type", sa.String(32), nullable=False),
        sa.Column("source_module", sa.String(64), nullable=False),
        sa.Column("rule_version", sa.String(32), nullable=False),
        sa.Column("score_snapshot", sa.JSON, nullable=True),
        sa.Column("risk_snapshot", sa.JSON, nullable=True),
        sa.Column("decision", sa.String(32), nullable=False),
        sa.Column("reason", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_signal_events_trade_date", "signal_events", ["trade_date"])
    op.create_index("ix_signal_events_symbol", "signal_events", ["symbol"])
    op.create_index("ix_signal_events_trade_date_symbol", "signal_events", ["trade_date", "symbol"])

    op.create_table(
        "review_daily",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("review_date", sa.Date, unique=True, nullable=False),
        sa.Column("rule_version", sa.String(32), nullable=False),
        sa.Column("total_signals", sa.Integer, nullable=False, server_default=sa.text("0")),
        sa.Column("valid_signals", sa.Integer, nullable=False, server_default=sa.text("0")),
        sa.Column("hit_count", sa.Integer, nullable=False, server_default=sa.text("0")),
        sa.Column("miss_count", sa.Integer, nullable=False, server_default=sa.text("0")),
        sa.Column("avg_return_1d", sa.Numeric(12, 4), nullable=True),
        sa.Column("avg_return_3d", sa.Numeric(12, 4), nullable=True),
        sa.Column("avg_return_5d", sa.Numeric(12, 4), nullable=True),
        sa.Column("summary", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("review_daily")
    op.drop_table("signal_events")
    op.drop_table("positions")
    op.drop_table("daily_bars")
    op.drop_table("stocks")
