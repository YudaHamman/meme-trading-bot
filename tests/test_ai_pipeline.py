import asyncio
from datetime import datetime, timezone
from decimal import Decimal

from app.ai.claude import ClaudeClient
from app.market.analysis.intelligence import MarketIntelligence
from app.market.models import TokenMarket


async def main():

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

    intelligence = MarketIntelligence()

    results = intelligence.analyze_tokens(
        [token]
    )

    result = results[0]

    market_intelligence = {
        "token": {
            "address": result["token"].address,
            "symbol": result["token"].symbol,
            "name": result["token"].name,
        },

        "system_score": str(
            result["score"]
        ),

        "market_analysis": {
            "momentum_score": str(
                result["analysis"].momentum_score
            ),
            "volume_score": str(
                result["analysis"].volume_score
            ),
            "pressure_score": str(
                result["analysis"].pressure_score
            ),
            "liquidity_score": str(
                result["analysis"].liquidity_score
            ),
            "overall_score": str(
                result["analysis"].overall_score
            ),
        },

        "market_data": {
            "price_usd": str(token.price_usd),
            "liquidity_usd": str(token.liquidity_usd),
            "volume_5m_usd": str(token.volume_5m_usd),
            "volume_1h_usd": str(token.volume_1h_usd),
            "volume_24h_usd": str(token.volume_24h_usd),
            "price_change_5m": str(token.price_change_5m),
            "price_change_1h": str(token.price_change_1h),
            "price_change_24h": str(token.price_change_24h),
            "buys_5m": token.buys_5m,
            "sells_5m": token.sells_5m,
        },
    }

    claude = ClaudeClient()

    try:

        analysis = await claude.analyze_market(
            market_intelligence
        )

        print()
        print("================================")
        print("       AI MARKET DECISION")
        print("================================")
        print()

        print(f"Token      : {token.symbol}")
        print(f"Score      : {result['score']}")
        print(f"Decision   : {analysis.decision}")
        print(f"Confidence : {analysis.confidence}%")
        print(f"Risk       : {analysis.risk_level}")
        print(f"Momentum   : {analysis.momentum}")

        print()
        print("Reasoning:")
        print(f"  {analysis.reasoning}")

        print()
        print("Invalidation:")

        for index, condition in enumerate(
            analysis.invalidation,
            start=1,
        ):
            print(
                f"  {index}. {condition}"
            )

        print()
        print("================================")
        print("       AI PIPELINE OK")
        print("================================")

    finally:

        await claude.close()


if __name__ == "__main__":
    asyncio.run(main())