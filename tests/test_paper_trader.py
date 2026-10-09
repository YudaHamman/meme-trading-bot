from decimal import Decimal

from app.execution.paper_trader import PaperTrader
from app.execution.position_monitor import PositionMonitor


def test_open_position():
    trader = PaperTrader()

    result = trader.open_position(
        token_address="TEST_TOKEN",
        symbol="TEST",
        entry_price=Decimal("0.0001"),
        position_size_usd=Decimal("25"),
    )

    position = trader.positions["TEST_TOKEN"]

    assert result.action == "OPEN"
    assert position.status == "OPEN"
    assert position.position_size_usd == Decimal("25")
    assert position.entry_price == Decimal("0.0001")
    assert position.take_profit_price == Decimal("0.00012")
    assert position.stop_loss_price == Decimal("0.00009")


def test_position_monitor_hold():
    trader = PaperTrader()
    monitor = PositionMonitor(trader)

    trader.open_position(
        token_address="TEST_TOKEN",
        symbol="TEST",
        entry_price=Decimal("0.0001"),
        position_size_usd=Decimal("25"),
    )

    result = monitor.update_position(
        token_address="TEST_TOKEN",
        current_price=Decimal("0.000105"),
    )

    assert result.action == "HOLD"

    position = trader.positions["TEST_TOKEN"]

    assert position.status == "OPEN"


def test_take_profit():
    trader = PaperTrader()
    monitor = PositionMonitor(trader)

    trader.open_position(
        token_address="TEST_TOKEN",
        symbol="TEST",
        entry_price=Decimal("0.0001"),
        position_size_usd=Decimal("25"),
    )

    result = monitor.update_position(
        token_address="TEST_TOKEN",
        current_price=Decimal("0.00012"),
    )

    assert result.action == "TP"

    position = trader.positions["TEST_TOKEN"]

    assert position.status == "CLOSED"
    assert position.pnl_percent == Decimal("20")


def test_stop_loss():
    trader = PaperTrader()
    monitor = PositionMonitor(trader)

    trader.open_position(
        token_address="TEST_TOKEN",
        symbol="TEST",
        entry_price=Decimal("0.0001"),
        position_size_usd=Decimal("25"),
    )

    result = monitor.update_position(
        token_address="TEST_TOKEN",
        current_price=Decimal("0.00009"),
    )

    assert result.action == "SL"

    position = trader.positions["TEST_TOKEN"]

    assert position.status == "CLOSED"
    assert position.pnl_percent == Decimal("-10")


def test_duplicate_position_rejected():
    trader = PaperTrader()

    trader.open_position(
        token_address="TEST_TOKEN",
        symbol="TEST",
        entry_price=Decimal("0.0001"),
        position_size_usd=Decimal("25"),
    )

    try:
        trader.open_position(
            token_address="TEST_TOKEN",
            symbol="TEST",
            entry_price=Decimal("0.0001"),
            position_size_usd=Decimal("25"),
        )

        assert False, "Expected ValueError"

    except ValueError as exc:
        assert str(exc) == "Position already exists"


def test_invalid_entry_price_rejected():
    trader = PaperTrader()

    try:
        trader.open_position(
            token_address="TEST_TOKEN",
            symbol="TEST",
            entry_price=Decimal("0"),
            position_size_usd=Decimal("25"),
        )

        assert False, "Expected ValueError"

    except ValueError as exc:
        assert str(exc) == "Entry price must be greater than zero"