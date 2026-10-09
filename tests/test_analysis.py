from datetime import datetime, timezone
from decimal import Decimal

from app.market.analysis.engine import MarketAnalysisEngine
from app.market.models import TokenMarket


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


engine = MarketAnalysisEngine()

result = engine.analyze(token)


print("===== MARKET ANALYSIS =====")
print("Momentum :", result.momentum_score)
print("Volume   :", result.volume_score)
print("Pressure :", result.pressure_score)
print("Liquidity:", result.liquidity_score)
print("Overall  :", result.overall_score)


if result.overall_score > Decimal("80"):
    print("ANALYSIS OK")
else:
    print("ANALYSIS FAILED")