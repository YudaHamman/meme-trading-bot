from datetime import datetime, timezone
from decimal import Decimal

from app.ai.models import AIAnalysis
from app.market.models import TokenMarket
from app.risk.engine import RiskEngine


token = TokenMarket(
    address="TOKEN_A",
    symbol="MOON",
    name="Moon Token",

    price_usd=Decimal("0.001"),

    market_cap_usd=Decimal("500000"),
    liquidity_usd=Decimal("150000"),

    volume_5m_usd=Decimal("60000"),
    volume_1h_usd=Decimal("200000"),
    volume_24h_usd=Decimal("900000"),

    price_change_5m=Decimal("12"),
    price_change_1h=Decimal("25"),
    price_change_24h=Decimal("50"),

    buys_5m=80,
    sells_5m=20,

    dex="raydium",

    updated_at=datetime.now(timezone.utc),
)


ai_analysis = AIAnalysis(
    decision="BUY",
    confidence=85,
    risk_level="MEDIUM",
    momentum="BULLISH",
    reasoning="Strong momentum and buying pressure.",
    invalidation=[
        "Buying pressure weakens",
        "Liquidity decreases",
        "Volume collapses",
    ],
)


engine = RiskEngine()

result = engine.evaluate(
    token=token,
    ai_analysis=ai_analysis,
)


print()
print("=== RISK ENGINE ===")
print()

print("Approved       :", result.approved)
print("Decision       :", result.decision)
print("Position Size  :", result.position_size_usd)
print("Risk Level     :", result.risk_level)

print()
print("Reasons:")

for reason in result.reasons:
    print(f"  - {reason}")

print()

if result.approved:
    print("RISK ENGINE OK")
else:
    print("RISK ENGINE REJECTED")