from datetime import datetime, timezone
from decimal import Decimal

from app.market.models import TokenMarket
from app.market.scoring.engine import ScoringEngine


token = TokenMarket(
    address="TEST",
    symbol="TEST",
    name="Test Token",

    price_usd=Decimal("0.001"),

    market_cap_usd=Decimal("500000"),
    liquidity_usd=Decimal("100000"),

    volume_5m_usd=Decimal("50000"),
    volume_1h_usd=Decimal("100000"),
    volume_24h_usd=Decimal("500000"),

    price_change_5m=Decimal("10"),
    price_change_1h=Decimal("20"),
    price_change_24h=Decimal("30"),

    buys_5m=80,
    sells_5m=20,

    updated_at=datetime.now(timezone.utc),
)


engine = ScoringEngine()

result = engine.calculate(token)

print("TOKEN:", result.token.symbol)
print("SCORE:", result.score)

if result.score == Decimal("100"):
    print("SCORING OK")
else:
    print("SCORING FAILED")