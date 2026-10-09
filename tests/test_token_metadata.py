import asyncio

from app.market.providers.token_metadata import (
    TokenMetadataExtractor,
)


MINT_ADDRESS = (
    "7a61CnMjeGtEj7Ems5gRnyVXMnQGfDt6b259iGnZpump"
)


async def main():

    extractor = TokenMetadataExtractor()

    print(
        "GETTING TOKEN METADATA...",
        flush=True,
    )

    metadata = await extractor.get_metadata(
        MINT_ADDRESS
    )

    if metadata is None:

        print(
            "METADATA NOT FOUND",
            flush=True,
        )

        return

    print(
        "\nTOKEN METADATA",
        flush=True,
    )

    print(
        "MINT:",
        metadata["mint"],
        flush=True,
    )

    print(
        "NAME:",
        metadata["name"],
        flush=True,
    )

    print(
        "SYMBOL:",
        metadata["symbol"],
        flush=True,
    )

    print(
        "DECIMALS:",
        metadata["decimals"],
        flush=True,
    )

    print(
        "SUPPLY:",
        metadata["supply"],
        flush=True,
    )

    print(
        "URI:",
        metadata["uri"],
        flush=True,
    )

    print(
        "OWNER:",
        metadata["owner"],
        flush=True,
    )


if __name__ == "__main__":
    asyncio.run(main())