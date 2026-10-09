import asyncio

from app.market.providers.dexscreener import DexScreenerProvider
from app.market.normalizer import MarketNormalizer


async def main():
    provider = DexScreenerProvider()

    try:
        data = await provider.search("SOL")

        pairs = data.get("pairs", [])

        if not pairs:
            print("Tidak ada pair ditemukan.")
            return

        token = MarketNormalizer.from_dexscreener(pairs[0])

        print("\n===== TOKEN MARKET =====")
        print("Name       :", token.name)
        print("Symbol     :", token.symbol)
        print("Price      :", token.price_usd)
        print("Liquidity  :", token.liquidity_usd)
        print("Volume 5m  :", token.volume_5m_usd)
        print("Volume 1h  :", token.volume_1h_usd)
        print("Volume 24h :", token.volume_24h_usd)
        print("Buy 5m     :", token.buys_5m)
        print("Sell 5m    :", token.sells_5m)
        print("DEX        :", token.dex)

    finally:
        await provider.close()


if __name__ == "__main__":
    asyncio.run(main())