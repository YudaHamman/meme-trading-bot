import asyncio
from decimal import Decimal
from types import SimpleNamespace

from app.execution.paper_trader import PaperTrader
from app.execution.position_monitor import PositionMonitor
from app.execution.paper_position_service import (
    PaperPositionService,
)


class FakeMarketProvider:

    def __init__(self):
        self.prices = [
            Decimal("0.000105"),
            Decimal("0.00011"),
            Decimal("0.00012"),
        ]

    async def get_market(
        self,
        token_address: str,
    ):

        price = self.prices.pop(0)

        return SimpleNamespace(
            price_usd=price
        )


def test_position_service_reaches_take_profit():

    async def run():

        trader = PaperTrader()

        monitor = PositionMonitor(
            trader
        )

        provider = FakeMarketProvider()

        service = PaperPositionService(
            paper_trader=trader,
            position_monitor=monitor,
            market_provider=provider,
            poll_interval_seconds=0,
        )

        trader.open_position(
            token_address="TEST_TOKEN",
            symbol="TEST",
            entry_price=Decimal("0.0001"),
            position_size_usd=Decimal("25"),
        )

        await service.monitor_position(
            "TEST_TOKEN"
        )

        position = trader.positions[
            "TEST_TOKEN"
        ]

        assert position.status == "CLOSED"
        assert position.current_price == Decimal(
            "0.00012"
        )
        assert position.pnl_percent == Decimal(
            "20"
        )

    asyncio.run(run())


if __name__ == "__main__":
    print(
        "PAPER POSITION SERVICE TEST PASSED"
    )