from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class RiskConfig(BaseModel):
    max_position_usd: Decimal = Field(
        default=Decimal("25"),
        gt=Decimal("0"),
    )

    max_daily_loss_usd: Decimal = Field(
        default=Decimal("50"),
        gt=Decimal("0"),
    )

    min_confidence: Decimal = Field(
        default=Decimal("70"),
        ge=Decimal("0"),
        le=Decimal("100"),
    )

    max_risk_level: Literal[
        "LOW",
        "MEDIUM",
        "HIGH",
    ] = "MEDIUM"

    min_liquidity_usd: Decimal = Field(
        default=Decimal("10000"),
        ge=Decimal("0"),
    )


class RiskDecision(BaseModel):
    approved: bool

    decision: Literal[
        "APPROVE",
        "REJECT",
    ]

    position_size_usd: Decimal = Field(
        default=Decimal("0"),
        ge=Decimal("0"),
    )

    risk_level: Literal[
        "LOW",
        "MEDIUM",
        "HIGH",
    ]

    reasons: list[str]