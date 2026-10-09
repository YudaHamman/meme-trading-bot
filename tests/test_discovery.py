from datetime import datetime, timezone
from decimal import Decimal

from app.market.discovery import TokenDiscoveryEngine
from app.market.models import TokenMarket


def create_token(
    address: str,
    symbol: str,
    name: str,
):

    return TokenMarket(
        address=address,
        symbol=symbol,
        name=name,

        price_usd=Decimal("0.001"),
        market_cap_usd=Decimal("100000"),
        liquidity_usd=Decimal("50000"),

        volume_5m_usd=Decimal("10000"),
        volume_1h_usd=Decimal("50000"),
        volume_24h_usd=Decimal("100000"),

        price_change_5m=Decimal("5"),
        price_change_1h=Decimal("10"),
        price_change_24h=Decimal("20"),

        buys_5m=20,
        sells_5m=10,

        dex="raydium",

        updated_at=datetime.now(
            timezone.utc
        ),
    )


engine = TokenDiscoveryEngine()


tokens = [
    create_token(
        "ADDRESS_A",
        "MOON",
        "Moon Token",
    ),
    create_token(
        "ADDRESS_B",
        "CAT",
        "Cat Token",
    ),
]


print()
print("=== TOKEN DISCOVERY ===")
print()


# First discovery
new_tokens = engine.discover(
    tokens,
    source="dexscreener",
)

print(
    "New tokens:",
    len(new_tokens),
)

for token in new_tokens:

    print(
        f"{token.symbol:<8} "
        f"{token.name:<20} "
        f"source={token.source}"
    )


print()


# Run same tokens again
second_scan = engine.discover(
    tokens,
    source="dexscreener",
)

print(
    "Second scan:",
    len(second_scan),
)


if (
    len(new_tokens) == 2
    and len(second_scan) == 0
):

    print()
    print("TOKEN DISCOVERY OK")

else:

    print()
    print("TOKEN DISCOVERY FAILED")