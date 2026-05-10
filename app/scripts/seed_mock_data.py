"""Seed mock data into PostgreSQL.

Usage:
    python -m app.scripts.seed_mock_data
"""

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert

from app.db.session import SessionLocal
from app.db.models.stock import Stock
from app.db.models.daily_bar import DailyBar
from app.db.models.position import Position
from app.providers.mock.mock_market_data import MockMarketDataProvider


MOCK_POSITION_SYMBOLS = {"600519.SH", "000333.SZ", "300750.SZ"}


def seed() -> None:
    provider = MockMarketDataProvider()
    session = SessionLocal()

    try:
        # --- stocks ---
        stocks_data = provider.stocks()
        stocks_inserted = 0
        stocks_skipped = 0
        for s in stocks_data:
            stmt = (
                insert(Stock)
                .values(symbol=s.symbol, name=s.name, exchange=s.exchange, is_active=True)
                .on_conflict_do_nothing(index_elements=["symbol"])
            )
            result = session.execute(stmt)
            if result.rowcount > 0:
                stocks_inserted += 1
            else:
                stocks_skipped += 1
        session.commit()
        print(f"[stocks] inserted={stocks_inserted}, skipped={stocks_skipped}")

        # --- daily_bars ---
        bars_data = provider.daily_bars()
        bars_inserted = 0
        bars_skipped = 0
        for bar in bars_data:
            stmt = (
                insert(DailyBar)
                .values(
                    symbol=bar.symbol,
                    trade_date=bar.trade_date,
                    open=bar.open,
                    high=bar.high,
                    low=bar.low,
                    close=bar.close,
                    volume=bar.volume,
                    amount=bar.amount,
                )
                .on_conflict_do_nothing(
                    index_elements=["symbol", "trade_date"]
                )
            )
            result = session.execute(stmt)
            if result.rowcount > 0:
                bars_inserted += 1
            else:
                bars_skipped += 1
        session.commit()
        print(f"[daily_bars] inserted={bars_inserted}, skipped={bars_skipped}")

        # --- positions ---
        session.execute(
            select(func.count()).select_from(Position).where(
                Position.symbol.in_(MOCK_POSITION_SYMBOLS)
            )
        )
        session.query(Position).filter(
            Position.symbol.in_(MOCK_POSITION_SYMBOLS)
        ).delete(synchronize_session="fetch")
        session.commit()

        positions_data = provider.positions()
        positions_inserted = 0
        for p in positions_data:
            session.add(
                Position(
                    symbol=p.symbol,
                    quantity=p.quantity,
                    avg_cost=p.avg_cost,
                    position_date=p.position_date,
                )
            )
            positions_inserted += 1
        session.commit()
        print(f"[positions] inserted={positions_inserted} (mock positions replaced)")

        # --- verify row counts ---
        stock_count = session.query(func.count(Stock.id)).scalar()
        bar_count = session.query(func.count(DailyBar.id)).scalar()
        position_count = session.query(func.count(Position.id)).scalar()
        print(f"[summary] stocks={stock_count}, daily_bars={bar_count}, positions={position_count}")

    except Exception as exc:
        session.rollback()
        print(f"[seed] error: {exc}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
