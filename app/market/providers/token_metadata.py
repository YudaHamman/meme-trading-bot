import asyncio
from typing import Any

import httpx

from app.config.settings import settings


TOKEN_2022_PROGRAM_ID = (
    "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"
)


class TokenMetadataExtractor:

    async def get_metadata(
        self,
        mint: str,
    ) -> dict[str, Any] | None:

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getAccountInfo",
            "params": [
                mint,
                {
                    "encoding": "jsonParsed",
                    "commitment": "confirmed",
                },
            ],
        }

        async with httpx.AsyncClient(
            timeout=15
        ) as client:

            response = await client.post(
                settings.solana_rpc_url,
                json=payload,
            )

            response.raise_for_status()

            data = response.json()

        result = data.get("result")

        if not result:
            return None

        value = result.get("value")

        if not value:
            return None

        owner = value.get("owner")

        data_section = (
            value.get("data")
            or {}
        )

        parsed = (
            data_section.get("parsed")
            or {}
        )

        info = (
            parsed.get("info")
            or {}
        )

        if not info:
            return None

        decimals = info.get(
            "decimals"
        )

        supply = info.get(
            "supply"
        )

        extensions = (
            info.get("extensions")
            or []
        )

        token_metadata = None

        for extension in extensions:

            if not isinstance(
                extension,
                dict,
            ):
                continue

            if extension.get(
                "extension"
            ) == "tokenMetadata":

                token_metadata = (
                    extension.get(
                        "state"
                    )
                )

                break

        # =====================================
        # TOKEN-2022 METADATA
        # =====================================

        if token_metadata:

            name = (
                token_metadata.get(
                    "name"
                )
            )

            symbol = (
                token_metadata.get(
                    "symbol"
                )
            )

            uri = (
                token_metadata.get(
                    "uri"
                )
            )

            if name or symbol:

                return {
                    "mint": mint,
                    "name": name,
                    "symbol": symbol,
                    "decimals": decimals,
                    "supply": supply,
                    "uri": uri,
                    "owner": owner,
                }

        # =====================================
        # NO DIRECT METADATA
        # =====================================

        return None

    async def get_metadata_with_retry(
        self,
        mint: str,
        max_attempts: int = 10,
        delay_seconds: float = 1.0,
    ) -> dict[str, Any] | None:

        for attempt in range(
            1,
            max_attempts + 1,
        ):

            print(
                f"METADATA ATTEMPT "
                f"{attempt}/{max_attempts}"
            )

            try:

                metadata = (
                    await self.get_metadata(
                        mint
                    )
                )

                if metadata:

                    print(
                        "METADATA FOUND"
                    )

                    return metadata

            except Exception as exc:

                print(
                    "METADATA ERROR:",
                    exc
                )

            if attempt < max_attempts:

                await asyncio.sleep(
                    delay_seconds
                )

        print(
            "METADATA NOT FOUND "
            "AFTER RETRIES"
        )

        return None