from datetime import datetime, timezone
from decimal import Decimal

import asyncio

from app.ai.claude import (
    ClaudeAIEngine,
)

from app.market.models import TokenMarket

from app.market.scoring.engine import (
    ScoringEngine,
)

from app.market.analysis.intelligence import (
    MarketIntelligence,
)


async def main():

    # =====================================
    # TEST MARKET DATA
    # =====================================

    market = TokenMarket(

        address="TEST_MINT",

        symbol="APC",

        name="A Pons Coin",

        price_usd=Decimal(
            "0.00004712"
        ),

        market_cap_usd=Decimal(
            "0"
        ),

        liquidity_usd=Decimal(
            "16711.64"
        ),

        volume_5m_usd=Decimal(
            "793.33"
        ),

        volume_1h_usd=Decimal(
            "793.33"
        ),

        volume_24h_usd=Decimal(
            "793.33"
        ),

        price_change_5m=Decimal(
            "10"
        ),

        price_change_1h=Decimal(
            "10"
        ),

        price_change_24h=Decimal(
            "10"
        ),

        buys_5m=39,

        sells_5m=6,

        pair_address=(
            "TEST_PAIR"
        ),

        dex="pumpswap",

        updated_at=datetime.now(
            timezone.utc
        ),

        source="test",
    )

    # =====================================
    # SCORING
    # =====================================

    scoring = ScoringEngine()

    candidate = (
        scoring.calculate(
            market
        )
    )

    # =====================================
    # INTELLIGENCE
    # =====================================

    intelligence = (
        MarketIntelligence()
        .analyze(
            market
        )
    )

    # =====================================
    # PIPELINE RESULT
    # =====================================

    result = {

        "mint": (
            "TEST_MINT"
        ),

        "metadata": {
            "name": (
                "A Pons Coin"
            ),
            "symbol": "APC",
        },

        "market": market,

        "candidate": candidate,

        "intelligence": intelligence,
    }

    # =====================================
    # CLAUDE
    # =====================================

    engine = ClaudeAIEngine()

    print()
    print(
        "================================"
    )

    print(
        "CLAUDE LIVE ANALYSIS"
    )

    print(
        "================================"
    )

    print(
        "TOKEN:",
        market.name
    )

    print(
        "SYMBOL:",
        market.symbol
    )

    print(
        "SCORE:",
        candidate.score
    )

    print(
        "BUY PRESSURE:",
        intelligence[
            "buy_pressure"
        ]
    )

    print()

    analysis = (
        await engine.analyze(
            result
        )
    )

    # =====================================
    # RESULT
    # =====================================

    print(
        "DECISION:",
        analysis.decision
    )

    print(
        "CONFIDENCE:",
        analysis.confidence
    )

    print(
        "RISK:",
        analysis.risk_level
    )

    print(
        "MOMENTUM:",
        analysis.momentum
    )

    print()

    print(
        "REASONING:"
    )

    print(
        analysis.reasoning
    )

    print()

    print(
        "INVALIDATION:"
    )

    for item in (
        analysis.invalidation
    ):

        print(
            "-",
            item
        )

    print()
    print(
        "================================"
    )

    print(
        "CLAUDE TEST PASSED"
    )

    print(
        "================================"
    )


if __name__ == "__main__":

    asyncio.run(
        main()
    )