from datetime import datetime, timezone
from decimal import Decimal

from app.market.analysis.intelligence import MarketIntelligence
from app.market.models import TokenMarket


tokens = [
    TokenMarket(
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
    ),
]


engine = MarketIntelligence()

results = engine.analyze_tokens(tokens)

print()
print("=== MARKET INTELLIGENCE ===")
print()

for result in results:

    token = result["token"]
    score = result["score"]
    analysis = result["analysis"]

    print(f"Token       : {token.symbol}")
    print(f"Score       : {score}")
    print(f"Momentum    : {analysis.momentum_score}")
    print(f"Volume      : {analysis.volume_score}")
    print(f"Pressure    : {analysis.pressure_score}")
    print(f"Liquidity   : {analysis.liquidity_score}")
    print(f"Overall     : {analysis.overall_score}")

print()
print("MARKET INTELLIGENCE OK")