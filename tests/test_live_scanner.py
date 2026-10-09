import asyncio
from decimal import Decimal

from app.market.providers.dexscreener import (
    DexScreenerProvider,
)
from app.market.scanner import TokenScanner


async def main():

    provider = DexScreenerProvider()

    scanner = TokenScanner(
        min_liquidity_usd=Decimal("10000"),
        min_volume_5m_usd=Decimal("5000"),
        min_buys_5m=5,
    )

    try:

        tokens = await provider.search_tokens(
            "SOL"
        )

        print()
        print("=== LIVE DEXSCREENER ===")
        print()

        print(
            "Tokens received:",
            len(tokens),
        )

        candidates = scanner.filter_candidates(
            tokens
        )

        print(
            "Candidates:",
            len(candidates),
        )

        print()

        for token in candidates[:10]:

            print(
                f"{token.symbol:<12} "
                f"Liquidity=${token.liquidity_usd} "
                f"Volume5m=${token.volume_5m_usd} "
                f"Buys={token.buys_5m} "
                f"Sells={token.sells_5m}"
            )

        print()

        if tokens:
            print("LIVE MARKET DATA OK")
        else:
            print("NO MARKET DATA")

    finally:

        await provider.close()


if __name__ == "__main__":
    asyncio.run(main())