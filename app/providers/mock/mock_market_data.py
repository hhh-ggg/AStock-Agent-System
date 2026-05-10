import random
from datetime import date, timedelta
from decimal import Decimal
from typing import NamedTuple

MOCK_SEED = 42
MOCK_TRADING_DAYS = 60

StockDef = NamedTuple("StockDef", [("symbol", str), ("name", str), ("exchange", str)])

STOCK_DEFINITIONS: list[StockDef] = [
    StockDef("600000.SH", "浦发银行", "SH"),
    StockDef("600519.SH", "贵州茅台", "SH"),
    StockDef("601318.SH", "中国平安", "SH"),
    StockDef("000001.SZ", "平安银行", "SZ"),
    StockDef("000333.SZ", "美的集团", "SZ"),
    StockDef("000858.SZ", "五粮液", "SZ"),
    StockDef("002415.SZ", "海康威视", "SZ"),
    StockDef("300750.SZ", "宁德时代", "SZ"),
]


class DailyBarRow(NamedTuple):
    symbol: str
    trade_date: date
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    amount: Decimal


class PositionRow(NamedTuple):
    symbol: str
    quantity: Decimal
    avg_cost: Decimal
    position_date: date


class MockMarketDataProvider:

    def __init__(self, seed: int = MOCK_SEED):
        self.seed = seed
        self._rng = random.Random(seed)

    def stocks(self) -> list[StockDef]:
        return list(STOCK_DEFINITIONS)

    def daily_bars(self) -> list[DailyBarRow]:
        rng = random.Random(self.seed)
        bars: list[DailyBarRow] = []
        end_date = date(2026, 5, 8)
        trading_dates = self._generate_trading_dates(end_date, MOCK_TRADING_DAYS)

        for stock in STOCK_DEFINITIONS:
            base_price = rng.uniform(8.0, 200.0)
            price = base_price
            for td in trading_dates:
                daily_return = rng.uniform(-0.04, 0.045)
                close = round(price * (1 + daily_return), 2)
                intraday_range = close * rng.uniform(0.005, 0.03)
                open_ = round(close - rng.uniform(-intraday_range * 0.5, intraday_range * 0.5), 2)
                high = round(max(open_, close) + abs(rng.uniform(0, intraday_range * 0.6)), 2)
                low = round(min(open_, close) - abs(rng.uniform(0, intraday_range * 0.6)), 2)
                volume = round(rng.uniform(100000, 5000000), 2)

                bars.append(
                    DailyBarRow(
                        symbol=stock.symbol,
                        trade_date=td,
                        open=Decimal(str(open_)),
                        high=Decimal(str(high)),
                        low=Decimal(str(low)),
                        close=Decimal(str(close)),
                        volume=Decimal(str(volume)),
                        amount=Decimal(str(round(close * volume, 2))),
                    )
                )
                price = close

        return bars

    def positions(self) -> list[PositionRow]:
        return [
            PositionRow(
                symbol="600519.SH",
                quantity=Decimal("200"),
                avg_cost=Decimal("1680.50"),
                position_date=date(2026, 4, 15),
            ),
            PositionRow(
                symbol="000333.SZ",
                quantity=Decimal("1000"),
                avg_cost=Decimal("52.30"),
                position_date=date(2026, 5, 4),
            ),
            PositionRow(
                symbol="300750.SZ",
                quantity=Decimal("500"),
                avg_cost=Decimal("198.00"),
                position_date=date(2026, 3, 20),
            ),
        ]

    @staticmethod
    def _generate_trading_dates(end: date, count: int) -> list[date]:
        dates: list[date] = []
        current = end
        while len(dates) < count:
            if current.weekday() < 5:
                dates.append(current)
            current = current - timedelta(days=1)
        dates.reverse()
        return dates
