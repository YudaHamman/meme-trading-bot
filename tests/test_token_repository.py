from datetime import datetime, timezone
from decimal import Decimal

from app.database.models import initialize_database
from app.database.token_repository import TokenRepository
from app.market.models import TokenMarket


initialize_database()

token = TokenMarket(
    address="TEST_DB_TOKEN",
    symbol="DBTEST",
    name="Database Test Token",

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


repository = TokenRepository()

repository.save_token(token)

result = repository.get_token(
    "TEST_DB_TOKEN"
)


print()
print("=== TOKEN REPOSITORY ===")
print()

if result:

    print("Address :", result["address"])
    print("Symbol  :", result["symbol"])
    print("Name    :", result["name"])
    print("DEX     :", result["dex"])

    print()
    print("TOKEN REPOSITORY OK")

else:

    print()
    print("TOKEN REPOSITORY FAILED")