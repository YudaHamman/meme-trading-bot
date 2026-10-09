import asyncio

from app.market.providers.dexscreener import (
    DexScreenerProvider,
)
from app.market.scoring.engine import (
    ScoringEngine,
)


MINT = (
    "DtLQnXRu5FM2Rm3dw7RJd8BbH6xc2faY4W6Whgz8pump"
)


async def main():

    provider = DexScreenerProvider()

    scoring = ScoringEngine()

    print()
    print("GETTING MARKET DATA...")
    print("MINT:", MINT)
    print()

    market = await provider.get_market(
        MINT
    )

    if not market:

        print(
            "MARKET DATA NOT FOUND"
        )

        return

    print("MARKET DATA FOUND")
    print()

    print(
        "TOKEN:",
        market.name
    )

    print(
        "SYMBOL:",
        market.symbol
    )

    print(
        "PRICE:",
        market.price_usd
    )

    print(
        "LIQUIDITY:",
        market.liquidity_usd
    )

    print(
        "VOLUME 5M:",
        market.volume_5m_usd
    )

    print(
        "PRICE CHANGE 5M:",
        market.price_change_5m
    )

    print(
        "BUYS 5M:",
        market.buys_5m
    )

    print(
        "SELLS 5M:",
        market.sells_5m
    )

    print()
    print("CALCULATING SCORE...")

    candidate = scoring.calculate(
        market
    )

    print()
    print("SCORING RESULT")
    print(
        "TOKEN:",
        candidate.token.symbol
    )

    print(
        "SCORE:",
        candidate.score
    )

    print()
    print("TEST PASSED")


if __name__ == "__main__":

    asyncio.run(
        main()
    )