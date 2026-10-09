import asyncio

from app.market.providers.dexscreener import DexScreenerProvider


async def test_dexscreener():
    provider = DexScreenerProvider()

    try:
        data = await provider.search("SOL")

        assert "pairs" in data

        print("API OK")
        print("Pairs:", len(data["pairs"]))

    finally:
        await provider.close()


if __name__ == "__main__":
    asyncio.run(test_dexscreener())