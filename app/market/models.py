from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class TokenMarket(BaseModel):
    address: str
    symbol: str
    name: str

    price_usd: Decimal = Field(default=Decimal("0"))
    market_cap_usd: Decimal = Field(default=Decimal("0"))
    liquidity_usd: Decimal = Field(default=Decimal("0"))

    volume_5m_usd: Decimal = Field(default=Decimal("0"))
    volume_1h_usd: Decimal = Field(default=Decimal("0"))
    volume_24h_usd: Decimal = Field(default=Decimal("0"))

    price_change_5m: Decimal = Field(default=Decimal("0"))
    price_change_1h: Decimal = Field(default=Decimal("0"))
    price_change_24h: Decimal = Field(default=Decimal("0"))

    buys_5m: int = 0
    sells_5m: int = 0

    pair_address: str | None = None
    dex: str | None = None

    updated_at: datetime
    launch_timestamp: datetime | None = None
    source: str | None = None