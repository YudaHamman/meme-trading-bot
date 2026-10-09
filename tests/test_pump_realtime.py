import asyncio
import json

from app.market.providers.solana_ws import SolanaWebSocket
from app.market.providers.pump_parser import PumpEventParser


PUMP_PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"


async def main():

    ws = SolanaWebSocket()

    try:

        print("CONNECTING...", flush=True)

        await ws.connect()

        print("CONNECTED", flush=True)

        response = await ws.logs_subscribe(
            PUMP_PROGRAM_ID
        )

        print("SUBSCRIBED:", flush=True)
        print(
            json.dumps(response, indent=2),
            flush=True
        )

        print("\nWAITING FOR PUMP EVENTS...\n", flush=True)

        async with asyncio.timeout(30):

            async for event in ws.listen():

                parsed = PumpEventParser.parse(event)

                if parsed:

                    print(
                        "PUMP EVENT DETECTED:",
                        flush=True
                    )

                    print(
                        json.dumps(
                            parsed,
                            indent=2,
                            default=str
                        ),
                        flush=True
                    )

    except TimeoutError:

        print(
            "\n30 SECONDS FINISHED.",
            flush=True
        )

    finally:

        await ws.close()


if __name__ == "__main__":
    asyncio.run(main())