import asyncio

from app.ai.claude import ClaudeClient


async def main():

    claude = ClaudeClient()

    market_data = {
        "address": "TEST_TOKEN_ADDRESS",
        "symbol": "TEST",
        "name": "Test Meme Token",
        "price_usd": "0.000125",
        "market_cap_usd": "250000",
        "liquidity_usd": "75000",
        "volume_5m_usd": "25000",
        "volume_1h_usd": "85000",
        "volume_24h_usd": "350000",
        "price_change_5m": "8.5",
        "price_change_1h": "14.2",
        "price_change_24h": "35.8",
        "buys_5m": 85,
        "sells_5m": 35,
        "dex": "raydium",
    }

    try:

        analysis = await claude.analyze_token(
            market_data
        )

        print()
        print("=== CLAUDE ANALYSIS ===")
        print()
        print(f"Token      : {market_data['symbol']}")
        print(f"Decision   : {analysis.decision}")
        print(f"Confidence : {analysis.confidence}%")
        print(f"Risk       : {analysis.risk_level}")
        print(f"Momentum   : {analysis.momentum}")
        print()
        print("Reasoning:")
        print(f"  {analysis.reasoning}")
        print()
        print("Invalidation:")

        for index, condition in enumerate(
            analysis.invalidation,
            start=1,
        ):
            print(f"  {index}. {condition}")

        print()
        print("CLAUDE ANALYSIS OK")

    finally:

        await claude.close()


if __name__ == "__main__":
    asyncio.run(main())