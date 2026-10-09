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
    print("CHECKING DEXSCREENER...")
    print("MINT:", MINT)
    print()

    pairs = await provider.get_token_pairs(
        MINT
    )

    print(
        "PAIRS FOUND:",
        len(pairs)
    )

    for pair in pairs:

        print()
        print(
            "DEX:",
            pair.get("dexId")
        )

        print(
            "PAIR:",
            pair.get("pairAddress")
        )

        print(
            "PRICE:",
            pair.get("priceUsd")
        )

        liquidity = (
            pair.get("liquidity")
            or {}
        )

        print(
            "LIQUIDITY USD:",
            liquidity.get("usd")
        )

        volume = (
            pair.get("volume")
            or {}
        )

        print(
            "VOLUME 24H:",
            volume.get("h24")
        )

    print()
    print("GETTING BEST SOLANA PAIR...")

    best_pair = await provider.get_best_pair(
        MINT
    )

    if not best_pair:

        print()
        print(
            "NO SOLANA PAIR FOUND"
        )

        return

    print()
    print("BEST PAIR FOUND")
    print(
        "DEX:",
        best_pair.get("dexId")
    )

    print(
        "PAIR:",
        best_pair.get("pairAddress")
    )

    print(
        "PRICE:",
        best_pair.get("priceUsd")
    )

    liquidity = (
        best_pair.get("liquidity")
        or {}
    )

    print(
        "LIQUIDITY USD:",
        liquidity.get("usd")
    )

    print()
    print("TEST PASSED")


if __name__ == "__main__":

    asyncio.run(
        main()
    )