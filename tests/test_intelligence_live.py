from datetime import datetime, timezone
from decimal import Decimal

from app.market.models import TokenMarket
from app.market.analysis.intelligence import (
    MarketIntelligence,
)


def main():

    token = TokenMarket(

        address="TEST_MINT",

        symbol="TEST",

        name="Test Token",

        price_usd=Decimal(
            "0.000004461"
        ),

        market_cap_usd=Decimal("0"),

        liquidity_usd=Decimal("0"),

        volume_5m_usd=Decimal(
            "893.38"
        ),

        volume_1h_usd=Decimal(
            "893.38"
        ),

        volume_24h_usd=Decimal(
            "893.38"
        ),

        price_change_5m=Decimal("0"),

        price_change_1h=Decimal("0"),

        price_change_24h=Decimal("0"),

        buys_5m=10,

        sells_5m=2,

        pair_address="TEST_PAIR",

        dex="pumpfun",

        updated_at=datetime.now(
            timezone.utc
        ),

        source="test",
    )

    intelligence = (
        MarketIntelligence()
    )

    result = (
        intelligence.analyze(
            token
        )
    )

    print()
    print(
        "================================"
    )

    print(
        "MARKET INTELLIGENCE TEST"
    )

    print(
        "================================"
    )

    print(
        "MOMENTUM:",
        result["momentum"]
    )

    print(
        "BUY PRESSURE:",
        result["buy_pressure"],
        "%"
    )

    print(
        "BUY PRESSURE STATUS:",
        result[
            "buy_pressure_status"
        ]
    )

    print(
        "VOLUME STATUS:",
        result[
            "volume_status"
        ]
    )

    print(
        "LIQUIDITY STATUS:",
        result[
            "liquidity_status"
        ]
    )

    print(
        "TRANSACTIONS 5M:",
        result[
            "total_transactions_5m"
        ]
    )

    print(
        "RED FLAGS:",
        result["red_flags"]
    )

    print(
        "================================"
    )

    assert (
        result["buy_pressure"]
        == Decimal(
            "83.33333333333333333333333333"
        )
    )

    assert (
        result["buy_pressure_status"]
        == "VERY_STRONG"
    )

    assert (
        result["volume_status"]
        == "LOW"
    )

    assert (
        result["liquidity_status"]
        == "UNKNOWN"
    )

    assert (
        result["total_transactions_5m"]
        == 12
    )

    assert (
        "NO_LIQUIDITY_DATA"
        in result["red_flags"]
    )

    print(
        "TEST PASSED"
    )


if __name__ == "__main__":

    main()