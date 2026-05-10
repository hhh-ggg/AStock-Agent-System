import pytest

from app.providers.mock.mock_market_data import (
    MockMarketDataProvider,
    MOCK_TRADING_DAYS,
    STOCK_DEFINITIONS,
)


@pytest.fixture
def provider() -> MockMarketDataProvider:
    return MockMarketDataProvider(seed=42)


def test_stock_count(provider):
    stocks = provider.stocks()
    assert len(stocks) == 8


def test_stock_fields_complete(provider):
    for stock in provider.stocks():
        assert stock.symbol
        assert stock.name
        assert stock.exchange
        assert stock.symbol.endswith(".SH") or stock.symbol.endswith(".SZ")


def test_daily_bars_not_empty(provider):
    bars = provider.daily_bars()
    assert len(bars) == len(STOCK_DEFINITIONS) * MOCK_TRADING_DAYS
    symbols = {b.symbol for b in bars}
    assert symbols == {s.symbol for s in STOCK_DEFINITIONS}


def test_daily_bar_fields_complete(provider):
    bar = provider.daily_bars()[0]
    assert bar.symbol
    assert bar.trade_date
    assert bar.open is not None
    assert bar.high is not None
    assert bar.low is not None
    assert bar.close is not None
    assert bar.volume is not None
    assert bar.amount is not None
    assert bar.high >= bar.low
    assert bar.high >= bar.open
    assert bar.high >= bar.close
    assert bar.low <= bar.open
    assert bar.low <= bar.close


def test_daily_bars_repeatable(provider):
    bars_a = provider.daily_bars()
    bars_b = MockMarketDataProvider(seed=42).daily_bars()
    for i in range(len(bars_a)):
        assert bars_a[i].symbol == bars_b[i].symbol
        assert bars_a[i].trade_date == bars_b[i].trade_date
        assert bars_a[i].close == bars_b[i].close


def test_positions_count(provider):
    positions = provider.positions()
    assert len(positions) == 3


def test_position_fields_complete(provider):
    for p in provider.positions():
        assert p.symbol
        assert p.quantity > 0
        assert p.avg_cost > 0
        assert p.position_date


def test_stock_definitions_known_symbols():
    symbols = [s.symbol for s in STOCK_DEFINITIONS]
    assert "600519.SH" in symbols
    assert "000333.SZ" in symbols
    assert "300750.SZ" in symbols
