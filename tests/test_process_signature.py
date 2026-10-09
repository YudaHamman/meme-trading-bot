import asyncio

from app.core.live_discovery_pipeline import (
    LiveDiscoveryPipeline,
)


SIGNATURE = (
    "3oynv92gZZ3KbDoq8ckjhf7msqsQBbTT29m19AfuAB9EQZo2vg8bB1wT96E9dxFrbFheDxUf2LWpLGaRe1pust53"
)


async def main():

    pipeline = LiveDiscoveryPipeline()

    print()
    print("================================")
    print("PROCESS SIGNATURE TEST")
    print("================================")
    print()

    result = await pipeline.process_signature(
        SIGNATURE
    )

    print()

    if result:

        print("================================")
        print("PROCESS SUCCESS")
        print("================================")

        print(
            "MINT:",
            result["mint"]
        )

        print(
            "AI:",
            result["ai_analysis"].decision
        )

        print(
            "CONFIDENCE:",
            result["ai_analysis"].confidence
        )

        print(
            "RISK:",
            result["risk_decision"].decision
        )

        if result.get("paper_trade"):

            print(
                "PAPER TRADE:",
                result["paper_trade"].action
            )

        else:

            print(
                "PAPER TRADE: NONE"
            )

    else:

        print("PROCESS FAILED")


if __name__ == "__main__":

    asyncio.run(main())