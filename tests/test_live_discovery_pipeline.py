import asyncio

from app.core.live_discovery_pipeline import (
    LiveDiscoveryPipeline,
)


async def main():

    pipeline = LiveDiscoveryPipeline()

    print()
    print("================================")
    print("LIVE DISCOVERY PIPELINE")
    print("================================")
    print()
    print("LISTENING FOR NEW CREATE...")
    print("Press CTRL+C to stop")
    print()

    async for result in pipeline.listen(
        duration=120
    ):

        metadata = result[
            "metadata"
        ]

        market = result[
            "market"
        ]

        candidate = result[
            "candidate"
        ]

        print()
        print("================================")
        print("🔥 NEW TOKEN ANALYZED")
        print("================================")

        print(
            "NAME:",
            metadata.get("name")
        )

        print(
            "SYMBOL:",
            metadata.get("symbol")
        )

        print(
            "MINT:",
            result["mint"]
        )

        print()
        print("MARKET")

        print(
            "DEX:",
            market.dex
        )

        print(
            "PAIR:",
            market.pair_address
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
            "BUYS 5M:",
            market.buys_5m
        )

        print(
            "SELLS 5M:",
            market.sells_5m
        )

        print()
        print("SCORING")

        print(
            "SCORE:",
            candidate.score
        )

        print()
        print("================================")
        print("PIPELINE SUCCESS")
        print("================================")

        break


if __name__ == "__main__":

    try:

        asyncio.run(
            main()
        )

    except KeyboardInterrupt:

        print()
        print("STOPPED BY USER")