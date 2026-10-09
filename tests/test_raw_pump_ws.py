import asyncio

from app.market.providers.solana_ws import SolanaWebSocket
from app.market.providers.pump_create_detector import PumpCreateDetector


PUMP_PROGRAM_ID = (
    "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
)


async def main():

    ws = SolanaWebSocket()

    print()
    print("================================")
    print("PUMP CREATE WS TEST")
    print("================================")

    await ws.connect()

    try:

        response = await ws.logs_subscribe(
            PUMP_PROGRAM_ID
        )

        print("SUBSCRIBED:", response)
        print("WAITING FOR CREATE...")
        print()

        async with asyncio.timeout(60):

            async for event in ws.listen():

                if not PumpCreateDetector.is_create_event(
                    event
                ):
                    continue

                params = event.get(
                    "params",
                    {}
                )

                result = params.get(
                    "result",
                    {}
                )

                value = result.get(
                    "value",
                    {}
                )

                signature = value.get(
                    "signature"
                )

                instruction = (
                    PumpCreateDetector
                    .get_create_instruction(
                        event
                    )
                )

                print("================================")
                print("🔥 CREATE DETECTED")
                print("================================")
                print("SIGNATURE:", signature)
                print("INSTRUCTION:", instruction)
                print("================================")

                return

    except TimeoutError:

        print()
        print("❌ NO CREATE EVENT FOR 60 SECONDS")

    finally:

        await ws.close()


if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:

        print()
        print("STOPPED")