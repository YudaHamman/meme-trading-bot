import asyncio

import httpx

from app.config.settings import settings


SIGNATURE = (
    "42kFtZ4zZ2LXbvADFMfY8kGXvynZBa9Pp555wSpt2AcTtMjfTp9GZKNN9Qc9ipx6nR9NVH1uJZLsZFHDxNi7Vfoc"
)

async def main():

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [
            SIGNATURE,
            {
                "encoding": "jsonParsed",
                "commitment": "confirmed",
                "maxSupportedTransactionVersion": 0,
            },
        ],
    }

    print("REQUESTING TRANSACTION...", flush=True)

    async with httpx.AsyncClient(timeout=15) as client:

        response = await client.post(
            settings.solana_rpc_url,
            json=payload,
        )

        response.raise_for_status()

        data = response.json()

    result = data.get("result")

    if not result:
        print("TRANSACTION NOT FOUND", flush=True)
        return

    print("TRANSACTION FOUND", flush=True)

    meta = result.get("meta") or {}

    print("\nTOKEN BALANCES:\n", flush=True)

    for balance in meta.get("preTokenBalances", []):

        print("PRE:", flush=True)

        print(
            "  accountIndex:",
            balance.get("accountIndex"),
            flush=True,
        )

        print(
            "  mint:",
            balance.get("mint"),
            flush=True,
        )

        print(
            "  owner:",
            balance.get("owner"),
            flush=True,
        )

    for balance in meta.get("postTokenBalances", []):

        print("POST:", flush=True)

        print(
            "  accountIndex:",
            balance.get("accountIndex"),
            flush=True,
        )

        print(
            "  mint:",
            balance.get("mint"),
            flush=True,
        )

        print(
            "  owner:",
            balance.get("owner"),
            flush=True,
        )

    print("\nTRANSACTION ACCOUNTS:\n", flush=True)

    message = result["transaction"]["message"]

    for index, account in enumerate(
        message.get("accountKeys", [])
    ):

        if isinstance(account, dict):

            pubkey = account.get("pubkey")
            signer = account.get("signer")
            writable = account.get("writable")

        else:

            pubkey = account
            signer = None
            writable = None

        print(
            index,
            pubkey,
            "signer=",
            signer,
            "writable=",
            writable,
            flush=True,
        )


if __name__ == "__main__":
    asyncio.run(main())