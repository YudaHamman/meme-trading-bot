import asyncio
import json

from app.market.providers.pump_discovery import (
    PumpTokenDiscovery,
)


async def main():

    discovery = PumpTokenDiscovery()

    try:

        print(
            "CONNECTING...",
            flush=True,
        )

        await discovery.ws.connect()

        print(
            "CONNECTED",
            flush=True,
        )

        response = await discovery.ws.logs_subscribe(
            "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
        )

        print(
            "SUBSCRIBED:",
            response,
            flush=True,
        )

        print(
            "\nWAITING FOR ONE SUCCESSFUL EVENT...",
            flush=True,
        )

        async with asyncio.timeout(30):

            async for event in discovery.ws.listen():

                params = event.get("params", {})
                result = params.get("result", {})
                value = result.get("value", {})

                if value.get("err") is not None:
                    continue

                signature = value.get("signature")

                if not signature:
                    continue

                print(
                    "\nSUCCESSFUL EVENT:",
                    signature,
                    flush=True,
                )

                print(
                    "GETTING TRANSACTION...",
                    flush=True,
                )

                transaction = await discovery.get_transaction(
                    signature
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

                message = (
                    transaction
                    .get("transaction", {})
                    .get("message", {})
                )

                account_keys = message.get(
                    "accountKeys",
                    []
                )

                instructions = message.get(
                    "instructions",
                    []
                )

                meta = transaction.get(
                    "meta",
                    {}
                )

                inner_instructions = meta.get(
                    "innerInstructions",
                    []
                )

                print(
                    "\n========== ACCOUNT KEYS ==========",
                    flush=True,
                )

                for index, account in enumerate(
                    account_keys
                ):

                    if isinstance(account, dict):

                        print(
                            f"[{index}] "
                            f"{account.get('pubkey')} "
                            f"writable={account.get('writable')} "
                            f"signer={account.get('signer')}",
                            flush=True,
                        )

                    else:

                        print(
                            f"[{index}] {account}",
                            flush=True,
                        )

                print(
                    "\n========== MAIN INSTRUCTIONS ==========",
                    flush=True,
                )

                print(
                    json.dumps(
                        instructions,
                        indent=2,
                        default=str,
                    ),
                    flush=True,
                )

                print(
                    "\n========== INNER INSTRUCTIONS ==========",
                    flush=True,
                )

                print(
                    json.dumps(
                        inner_instructions,
                        indent=2,
                        default=str,
                    ),
                    flush=True,
                )

                print(
                    "\n========== LOGS ==========",
                    flush=True,
                )

                logs = meta.get(
                    "logMessages",
                    []
                )

                for log in logs or []:

                    print(
                        log,
                        flush=True,
                    )

                print(
                    "\n========== END TRANSACTION ==========",
                    flush=True,
                )

                return

    except TimeoutError:

        print(
            "\n30 SECONDS FINISHED.",
            flush=True,
        )

    finally:

        await discovery.ws.close()

        print(
            "WEBSOCKET CLOSED",
            flush=True,
        )


if __name__ == "__main__":
    asyncio.run(main())