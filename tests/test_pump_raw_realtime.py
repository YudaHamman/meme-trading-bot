import asyncio

from app.market.providers.solana_ws import SolanaWebSocket


PUMP_PROGRAM_ID = (
    "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
)


async def main():

    ws = SolanaWebSocket()

    await ws.connect()

    try:

        response = await ws.logs_subscribe(
            PUMP_PROGRAM_ID
        )

        print()
        print("SUBSCRIBED:")
        print(response)

        print()
        print("LISTENING RAW PUMP EVENTS...")
        print("Press CTRL+C to stop")
        print()

        count = 0

        async with asyncio.timeout(30):

            async for event in ws.listen():

                count += 1

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

                err = value.get(
                    "err"
                )

                logs = value.get(
                    "logs",
                    []
                )

                print()
                print(
                    "EVENT:",
                    count
                )

                print(
                    "SIGNATURE:",
                    signature
                )

                print(
                    "ERROR:",
                    err
                )

                print(
                    "LOG COUNT:",
                    len(logs)
                )

                for log in logs:

                    if (
                        "Instruction:" in log
                        or "Program "
                        in log
                    ):

                        print(
                            log
                        )

                if count >= 5:

                    break

    except TimeoutError:

        print()
        print(
            "30 SECOND TIMEOUT"
        )

        print(
            "EVENTS RECEIVED:",
            count
        )

    finally:

        await ws.close()

        print()
        print("WEBSOCKET CLOSED")


if __name__ == "__main__":

    try:

        asyncio.run(
            main()
        )

    except KeyboardInterrupt:

        print()
        print("STOPPED BY USER")