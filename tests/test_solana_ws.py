import asyncio

from app.market.providers.solana_ws import SolanaWebSocket


async def main():
    ws = SolanaWebSocket()

    try:
        await ws.connect()
        print("SOLANA WEBSOCKET OK")
    finally:
        await ws.close()


if __name__ == "__main__":
    asyncio.run(main())