import asyncio
import json

from app.market.providers.solana_ws import SolanaWebSocket


PUMP_PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"


async def main():

    ws = SolanaWebSocket()

    try:

        await ws.connect()

        response = await ws.logs_subscribe(
            PUMP_PROGRAM_ID
        )

        print("SUBSCRIBE RESPONSE:")
        print(json.dumps(response, indent=2))

        print("\nLISTENING FOR 30 SECONDS...\n")

        try:

            async with asyncio.timeout(30):

                async for event in ws.listen():

                    print(
                        json.dumps(
                            event,
                            indent=2
                        )
                    )

        except TimeoutError:

            print("\n30 SECONDS FINISHED.")

    finally:

        await ws.close()


if __name__ == "__main__":
    asyncio.run(main())