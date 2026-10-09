from decimal import Decimal

from app.execution.paper_trader import PaperTrader
from app.execution.position_monitor import PositionMonitor


trader = PaperTrader(
    take_profit_percent=Decimal("20"),
    stop_loss_percent=Decimal("10"),
)

monitor = PositionMonitor(trader)


print()
print("=== POSITION MONITOR ===")
print()


# Open position
trader.open_position(
    token_address="TOKEN_A",
    symbol="MOON",
    entry_price=Decimal("0.001"),
    position_size_usd=Decimal("25"),
)


# Price movement
prices = [
    Decimal("0.00105"),
    Decimal("0.00110"),
    Decimal("0.00115"),
    Decimal("0.00120"),
]


for price in prices:

    result = monitor.update_position(
        token_address="TOKEN_A",
        current_price=price,
    )

    print(
        f"Price={price} "
        f"Action={result.action} "
        f"PnL={result.pnl_percent}%"
    )

    if result.action == "TP":

        print()
        print("TAKE PROFIT TRIGGERED")
        break


position = trader.positions["TOKEN_A"]


print()
print("Final Status :", position.status)
print("Final PnL    :", position.pnl_percent)
print()


if (
    position.status == "CLOSED"
    and position.pnl_percent == Decimal("20")
):

    print("POSITION MONITOR OK")

else:

    print("POSITION MONITOR FAILED")