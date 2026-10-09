from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class AIAnalysis(BaseModel):

    decision: Literal[
        "BUY",
        "WATCH",
        "REJECT",
    ]

    confidence: Decimal = Field(
        ge=Decimal("0"),
        le=Decimal("100"),
    )

    risk_level: Literal[
        "LOW",
        "MEDIUM",
        "HIGH",
    ]

    momentum: Literal[
        "BULLISH",
        "NEUTRAL",
        "BEARISH",
    ]

    reasoning: str

    invalidation: list[str]


class AIAnalysisPayload(BaseModel):

    mint: str

    name: str

    symbol: str

    dex: str | None

    pair_address: str | None

    price_usd: Decimal

    market_cap_usd: Decimal

    liquidity_usd: Decimal

    volume_5m_usd: Decimal

    volume_1h_usd: Decimal

    volume_24h_usd: Decimal

    price_change_5m: Decimal

    price_change_1h: Decimal

    price_change_24h: Decimal

    buys_5m: int

    sells_5m: int

    score: Decimal

    momentum: str

    buy_pressure: Decimal

    buy_pressure_status: str

    volume_status: str

    liquidity_status: str

    total_transactions_5m: int

    red_flags: list[str]