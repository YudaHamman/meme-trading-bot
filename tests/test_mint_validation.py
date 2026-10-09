import asyncio

from app.market.providers.pump_discovery import (
    PumpTokenDiscovery,
)

from app.market.providers.mint_creation_detector import (
    MintCreationDetector,
)


SIGNATURE = (
    "2mfERhFV7hWQKsEmj44cfT5eUEfW2pRgM5RkxFo9sJPEYNUApq1F7iVmLQZ8Vo5d84DKBDBShmLjc8F7qcqKj6T4"
)


async def main():

    discovery = PumpTokenDiscovery()

    print(
        "GETTING TRANSACTION...",
        flush=True,
    )

    transaction = await discovery.get_transaction(
        SIGNATURE
    )

    if not transaction:

        print(
            "TRANSACTION NOT FOUND",
            flush=True,
        )

        return

    print(
        "TRANSACTION FOUND",
        flush=True,
    )

    create_instruction = (
        MintCreationDetector
        .find_create_instruction(
            transaction
        )
    )

    print(
        "\n========== RESULT ==========",
        flush=True,
    )

    if create_instruction:

        print(
            "CREATE V2: TRUE",
            flush=True,
        )

        print(
            "ACCOUNTS:",
            create_instruction.get(
                "accounts"
            ),
            flush=True,
        )

        print(
            "DATA:",
            create_instruction.get(
                "data"
            ),
            flush=True,
        )

    else:

        print(
            "CREATE V2: FALSE",
            flush=True,
        )


if __name__ == "__main__":
    asyncio.run(main())