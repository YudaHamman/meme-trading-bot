import asyncio
from decimal import Decimal

from app.core.logger import logger
from app.execution.paper_trader import PaperTrader
from app.execution.position_monitor import PositionMonitor
from app.market.providers.dexscreener import DexScreenerProvider


class PaperPositionService:

    def __init__(
        self,
        paper_trader: PaperTrader,
        position_monitor: PositionMonitor,
        market_provider: DexScreenerProvider,
        poll_interval_seconds: float = 5.0,
    ):
        self.paper_trader = paper_trader
        self.position_monitor = position_monitor
        self.market_provider = market_provider
        self.poll_interval_seconds = (
            poll_interval_seconds
        )

    async def monitor_position(
        self,
        token_address: str,
    ):

        logger.info(
            "Starting paper position monitor | token=%s",
            token_address,
        )

        while True:

            position = (
                self.paper_trader
                .positions
                .get(token_address)
            )

            if position is None:

                logger.warning(
                    "Paper position not found | token=%s",
                    token_address,
                )

                return

            if position.status == "CLOSED":

                logger.info(
                    "Paper position closed | token=%s",
                    token_address,
                )

                return

            try:

                market = (
                    await self.market_provider
                    .get_market(
                        token_address
                    )
                )

            except Exception as exc:

                logger.error(
                    "Market update error | token=%s | error=%s",
                    token_address,
                    exc,
                )

                await asyncio.sleep(
                    self.poll_interval_seconds
                )

                continue

            if market is None:

                logger.warning(
                    "Market unavailable | token=%s",
                    token_address,
                )

                await asyncio.sleep(
                    self.poll_interval_seconds
                )

                continue

            current_price = (
                Decimal(
                    str(
                        market.price_usd
                    )
                )
            )

            if current_price <= 0:

                logger.warning(
                    "Invalid market price | token=%s | price=%s",
                    token_address,
                    current_price,
                )

                await asyncio.sleep(
                    self.poll_interval_seconds
                )

                continue

            try:

                result = (
                    self.position_monitor
                    .update_position(
                        token_address=token_address,
                        current_price=current_price,
                    )
                )

            except Exception as exc:

                logger.error(
                    "Position update error | token=%s | error=%s",
                    token_address,
                    exc,
                )

                await asyncio.sleep(
                    self.poll_interval_seconds
                )

                continue

            logger.info(
                "Paper position update | token=%s | action=%s | price=%s",
                token_address,
                result.action,
                current_price,
            )

            if result.action in {
                "TP",
                "SL",
            }:

                logger.info(
                    "Paper position exited | token=%s | action=%s | pnl=%s | pnl%%=%s",
                    token_address,
                    result.action,
                    result.pnl_usd,
                    result.pnl_percent,
                )

                return

            await asyncio.sleep(
                self.poll_interval_seconds
            )