import asyncio
from typing import Any

import httpx

from app.config.settings import settings
from app.market.providers.solana_ws import SolanaWebSocket
from app.market.providers.token_metadata import TokenMetadataExtractor


PUMP_PROGRAM_ID = (
    "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
)


class PumpTokenDiscovery:

    def __init__(self):

        self.ws = SolanaWebSocket()
        self.metadata = TokenMetadataExtractor()

    async def get_transaction(
        self,
        signature: str,
    ) -> dict[str, Any] | None:

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [
                signature,
                {
                    "encoding": "jsonParsed",
                    "commitment": "confirmed",
                    "maxSupportedTransactionVersion": 0,
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

        return data.get("result")

    @staticmethod
    def find_mint(
        transaction: dict[str, Any],
    ) -> str | None:

        message = (
            transaction
            .get("transaction", {})
            .get("message", {})
        )

        accounts = message.get(
            "accountKeys",
            []
        )

        # Pump.fun mint biasanya berada
        # pada account yang writable dan
        # bukan program/system account.
        for account in accounts:

            if not isinstance(account, dict):
                continue

            pubkey = account.get("pubkey")

            if not pubkey:
                continue

            if not account.get("writable"):
                continue

            if pubkey.endswith("pump"):
                return pubkey

        return None

    async def process_signature(
        self,
        signature: str,
    ) -> dict[str, Any] | None:

        transaction = await self.get_transaction(
            signature
        )

        if not transaction:
            return None

        mint = self.find_mint(
            transaction
        )

        if not mint:
            return None

        metadata = await self.metadata.get_metadata(
            mint
        )

        if not metadata:
            return None

        return {
            "signature": signature,
            "mint": mint,
            **metadata,
        }

    async def listen(
        self,
        duration: int = 30,
    ):

        await self.ws.connect()

        try:

            response = await self.ws.logs_subscribe(
                PUMP_PROGRAM_ID
            )

            print(
                "SUBSCRIBED:",
                response,
                flush=True,
            )

            async with asyncio.timeout(
                duration
            ):

                async for event in self.ws.listen():

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

                    signature = value.get(
                        "signature"
                    )

                    if not signature:
                        continue

                    token = await self.process_signature(
                        signature
                    )

                    if token:

                        yield token

        except TimeoutError:

            return

        finally:

            await self.ws.close()