from datetime import datetime, timezone
from decimal import Decimal

from app.ai.payload import (
    AIPayloadBuilder,
)

from app.market.models import TokenMarket

from app.market.scoring.engine import (
    ScoringEngine,
)

from app.market.analysis.intelligence import (
    MarketIntelligence,
)


def main():

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

    scoring = ScoringEngine()

    candidate = scoring.calculate(
        market
    )

    intelligence = (
        MarketIntelligence()
        .analyze(
            market
        )
    )

    result = {

        "mint": "TEST_MINT",

        "metadata": {
            "name": "A Pons Coin",
            "symbol": "APC",
        },

        "market": market,

        "candidate": candidate,

        "intelligence": intelligence,
    }

    payload = (
        AIPayloadBuilder.build(
            result
        )
    )

    print()
    print(
        "================================"
    )

    print(
        "AI PAYLOAD TEST"
    )

    print(
        "================================"
    )

    print(
        "NAME:",
        payload.name
    )

    print(
        "SYMBOL:",
        payload.symbol
    )

    print(
        "DEX:",
        payload.dex
    )

    print(
        "PRICE:",
        payload.price_usd
    )

    print(
        "LIQUIDITY:",
        payload.liquidity_usd
    )

    print(
        "VOLUME 5M:",
        payload.volume_5m_usd
    )

    print(
        "BUYS 5M:",
        payload.buys_5m
    )

    print(
        "SELLS 5M:",
        payload.sells_5m
    )

    print(
        "SCORE:",
        payload.score
    )

    print(
        "MOMENTUM:",
        payload.momentum
    )

    print(
        "BUY PRESSURE:",
        payload.buy_pressure
    )

    print(
        "RED FLAGS:",
        payload.red_flags
    )

    print(
        "================================"
    )

    assert payload.name == (
        "A Pons Coin"
    )

    assert payload.symbol == "APC"

    assert payload.dex == "pumpswap"

    assert payload.buys_5m == 39

    assert payload.sells_5m == 6

    assert payload.score > 0

    assert payload.buy_pressure > 80

    print(
        "TEST PASSED"
    )


if __name__ == "__main__":

    main()