from datetime import datetime, timezone
from decimal import Decimal

from app.core.logger import logger
from app.execution.models import Position, TradeResult


class PaperTrader:

    def __init__(
        self,
        take_profit_percent: Decimal = Decimal("20"),
        stop_loss_percent: Decimal = Decimal("10"),
    ):
        self.take_profit_percent = take_profit_percent
        self.stop_loss_percent = stop_loss_percent

        self.positions: dict[str, Position] = {}

    def open_position(
        self,
        token_address: str,
        symbol: str,
        entry_price: Decimal,
        position_size_usd: Decimal,
    ) -> TradeResult:

        if token_address in self.positions:
            raise ValueError(
                "Position already exists"
            )

        if entry_price <= 0:
            raise ValueError(
                "Entry price must be greater than zero"
            )

        if position_size_usd <= 0:
            raise ValueError(
                "Position size must be greater than zero"
            )

        quantity = (
            position_size_usd
            / entry_price
        )

        take_profit_price = (
            entry_price
            * (
                Decimal("1")
                + self.take_profit_percent
                / Decimal("100")
            )
        )

        stop_loss_price = (
            entry_price
            * (
                Decimal("1")
                - self.stop_loss_percent
                / Decimal("100")
            )
        )

        now = datetime.now(timezone.utc)

        position = Position(
            token_address=token_address,
            symbol=symbol,
            entry_price=entry_price,
            current_price=entry_price,
            position_size_usd=position_size_usd,
            quantity=quantity,
            take_profit_price=take_profit_price,
            stop_loss_price=stop_loss_price,
            status="OPEN",
            opened_at=now,
        )

        self.positions[token_address] = position

        logger.info(
            "PAPER BUY %s | entry=%s | size=%s | TP=%s | SL=%s",
            symbol,
            entry_price,
            position_size_usd,
            take_profit_price,
            stop_loss_price,
        )

        return TradeResult(
            symbol=symbol,
            action="OPEN",
            price=entry_price,
            timestamp=now,
        )

    def update_price(
        self,
        token_address: str,
        current_price: Decimal,
    ) -> TradeResult:

        if current_price <= 0:
            raise ValueError(
                "Current price must be greater than zero"
            )

        if token_address not in self.positions:
            raise ValueError(
                "Position does not exist"
            )

        position = self.positions[token_address]

        if position.status == "CLOSED":
            raise ValueError(
                "Position is already closed"
            )

        position.current_price = current_price

        pnl_usd = (
            current_price
            - position.entry_price
        ) * position.quantity

        pnl_percent = (
            (
                current_price
                - position.entry_price
            )
            / position.entry_price
        ) * Decimal("100")

        position.pnl_usd = pnl_usd
        position.pnl_percent = pnl_percent

        action = "HOLD"

        if current_price >= position.take_profit_price:

            action = "TP"

            self._close_position(
                position
            )

        elif current_price <= position.stop_loss_price:

            action = "SL"

            self._close_position(
                position
            )

        logger.info(
            "PAPER %s %s | price=%s | pnl=%s | pnl%%=%s",
            action,
            position.symbol,
            current_price,
            pnl_usd,
            pnl_percent,
        )

        return TradeResult(
            symbol=position.symbol,
            action=action,
            price=current_price,
            pnl_usd=pnl_usd,
            pnl_percent=pnl_percent,
            timestamp=datetime.now(timezone.utc),
        )

    def _close_position(
        self,
        position: Position,
    ):

        position.status = "CLOSED"

        position.closed_at = (
            datetime.now(timezone.utc)
        )