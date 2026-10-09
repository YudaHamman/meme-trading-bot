import asyncio

from app.market.providers.dexscreener import (
    DexScreenerProvider,
)


MINT = (
    "DtLQnXRu5FM2Rm3dw7RJd8BbH6xc2faY4W6Whgz8pump"
)


async def main():

    provider = DexScreenerProvider()

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

    print("MARKET FOUND")
    print()

    print(
        "ADDRESS:",
        market.address
    )

    print(
        "NAME:",
        market.name
    )

    print(
        "SYMBOL:",
        market.symbol
    )

    print(
        "PRICE USD:",
        market.price_usd
    )

    print(
        "MARKET CAP USD:",
        market.market_cap_usd
    )

    print(
        "LIQUIDITY USD:",
        market.liquidity_usd
    )

    print(
        "VOLUME 5M:",
        market.volume_5m_usd
    )

    print(
        "VOLUME 1H:",
        market.volume_1h_usd
    )

    print(
        "VOLUME 24H:",
        market.volume_24h_usd
    )

    print(
        "PRICE CHANGE 5M:",
        market.price_change_5m
    )

    print(
        "PRICE CHANGE 1H:",
        market.price_change_1h
    )

    print(
        "PRICE CHANGE 24H:",
        market.price_change_24h
    )

    print(
        "BUYS 5M:",
        market.buys_5m
    )

    print(
        "SELLS 5M:",
        market.sells_5m
    )

    print(
        "PAIR:",
        market.pair_address
    )

    print(
        "DEX:",
        market.dex
    )

    print(
        "SOURCE:",
        market.source
    )

    print()
    print("TEST PASSED")


if __name__ == "__main__":

    asyncio.run(
        main()
    )