import asyncio

from app.market.providers.solana_ws import SolanaWebSocket
from app.market.providers.pump_create_detector import (
    PumpCreateDetector,
)
from app.market.providers.token_metadata import (
    TokenMetadataExtractor,
)
from app.market.providers.pump_discovery import (
    PumpTokenDiscovery,
)


PUMP_PROGRAM_ID = (
    "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
)


async def main():

    ws = SolanaWebSocket()

    metadata_extractor = TokenMetadataExtractor()

    discovery = PumpTokenDiscovery()

    await ws.connect()

    try:

        response = await ws.logs_subscribe(
            PUMP_PROGRAM_ID
        )

        print()
        print("SUBSCRIBED:")
        print(response)

        print()
        print("LISTENING FOR REAL CREATE...")
        print("Press CTRL+C to stop")
        print()

        async for event in ws.listen():

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

            if value.get("err") is not None:
                continue

            logs = value.get(
                "logs",
                []
            )

            if not logs:
                continue

            if not PumpCreateDetector.is_create_event(
                event
            ):
                continue

            signature = value.get(
                "signature"
            )

            if not signature:
                continue

            instruction = (
                PumpCreateDetector
                .get_create_instruction(
                    event
                )
            )

            print()
            print("================================")
            print("REAL CREATE DETECTED")
            print("SIGNATURE:", signature)
            print("INSTRUCTION:", instruction)
            print("================================")

            print()
            print("GETTING TRANSACTION...")

            transaction = await discovery.get_transaction(
                signature
            )

            if not transaction:

                print(
                    "TRANSACTION NOT FOUND"
                )

                continue

            print(
                "TRANSACTION FOUND"
            )

            mint = discovery.find_mint(
                transaction
            )

            print()
            print("MINT:", mint)

            if not mint:

                print(
                    "MINT NOT FOUND"
                )

                continue

            print()
            print("GETTING TOKEN METADATA...")

            metadata = (
                await metadata_extractor
                .get_metadata_with_retry(
                    mint,
                    max_attempts=5,
                    delay_seconds=0.5,
                )
            )

            if not metadata:

                print(
                    "METADATA NOT FOUND"
                )

                continue

            print()
            print("TOKEN FOUND")

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
                metadata.get("mint")
            )

            print(
                "DECIMALS:",
                metadata.get("decimals")
            )

            print(
                "SUPPLY:",
                metadata.get("supply")
            )

            print(
                "URI:",
                metadata.get("uri")
            )

            print()
            print("================================")
            print("CREATE PIPELINE SUCCESS")
            print("================================")

            break

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