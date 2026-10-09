from decimal import Decimal

from app.core.logger import logger
from app.execution.paper_trader import PaperTrader


class PositionMonitor:

    def __init__(
        self,
        paper_trader: PaperTrader,
    ):
        self.paper_trader = paper_trader

    def update_position(
        self,
        token_address: str,
        current_price: Decimal,
    ):

        logger.info(
            "Monitoring %s | price=%s",
            token_address,
            current_price,
        )

        result = self.paper_trader.update_price(
            token_address=token_address,
            current_price=current_price,
        )

        return result