import asyncio
import json

import httpx

from app.config.settings import settings


MINT_ADDRESS = (
    "7a61CnMjeGtEj7Ems5gRnyVXMnQGfDt6b259iGnZpump"
)


async def main():

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getAccountInfo",
        "params": [
            MINT_ADDRESS,
            {
                "encoding": "jsonParsed"
            }
        ]
    }

    print("CHECKING ACCOUNT...", flush=True)

    async with httpx.AsyncClient(timeout=15) as client:

        response = await client.post(
            settings.solana_rpc_url,
            json=payload,
        )

        response.raise_for_status()

        data = response.json()

    result = data.get("result")

    if not result:
        print("ACCOUNT NOT FOUND", flush=True)
        return

    value = result.get("value")

    if not value:
        print("ACCOUNT DATA NOT FOUND", flush=True)
        return

    print("\nACCOUNT OWNER:", flush=True)
    print(
        value.get("owner"),
        flush=True
    )

    print("\nACCOUNT DATA:", flush=True)

    print(
        json.dumps(
            value.get("data"),
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    asyncio.run(main())