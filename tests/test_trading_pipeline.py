import asyncio

from app.core.trading_pipeline import TradingPipeline


async def main():

    pipeline = TradingPipeline()

    await pipeline.run()


if __name__ == "__main__":
    asyncio.run(main())