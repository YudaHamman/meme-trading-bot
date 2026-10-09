from datetime import datetime
from decimal import Decimal
from typing import Any
from typing import Literal

from pydantic import BaseModel, Field


class Position(BaseModel):
    token_address: str
    symbol: str

    entry_price: Decimal = Field(
        gt=Decimal("0")
    )

    current_price: Decimal = Field(
        gt=Decimal("0")
    )

    position_size_usd: Decimal = Field(
        gt=Decimal("0")
    )

    quantity: Decimal = Field(
        gt=Decimal("0")
    )

    take_profit_price: Decimal = Field(
        gt=Decimal("0")
    )

    stop_loss_price: Decimal = Field(
        gt=Decimal("0")
    )

    status: Literal[
        "OPEN",
        "CLOSED",
    ] = "OPEN"

    opened_at: datetime
    closed_at: datetime | None = None

    pnl_usd: Decimal = Decimal("0")
    pnl_percent: Decimal = Decimal("0")


class TradeResult(BaseModel):
    symbol: str

    action: Literal[
        "OPEN",
        "TP",
        "SL",
        "HOLD",
    ]

    price: Decimal

    pnl_usd: Decimal = Decimal("0")
    pnl_percent: Decimal = Decimal("0")

    timestamp: datetime
    signature: str | None = None
    raw_result: dict[str, Any] | None = None
