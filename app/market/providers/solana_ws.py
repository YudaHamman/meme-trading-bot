import json

import websockets

from app.config.settings import settings
from app.core.logger import logger


class SolanaWebSocket:

    def __init__(self):

        self.url = settings.solana_ws_url

        self.websocket = None

    async def connect(self):

        if not self.url:

            raise ValueError(
                "SOLANA_WS_URL is not configured"
            )

        logger.info(
            "Connecting to Solana WebSocket"
        )

        self.websocket = await websockets.connect(
            self.url,
            ping_interval=20,
            ping_timeout=60,
            close_timeout=10,
            open_timeout=15,
            max_queue=1000,
        )

        logger.info(
            "Solana WebSocket connected"
        )

    async def close(self):

        if not self.websocket:

            return

        try:

            await self.websocket.close()

        except Exception as exc:

            logger.warning(
                "WebSocket close error: %s",
                exc
            )

        finally:

            self.websocket = None

            logger.info(
                "Solana WebSocket closed"
            )

    async def logs_subscribe(
        self,
        program_id: str,
    ):

        if not self.websocket:

            raise RuntimeError(
                "WebSocket is not connected"
            )

        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "logsSubscribe",
            "params": [
                {
                    "mentions": [
                        program_id
                    ]
                },
                {
                    "commitment": "processed"
                },
            ],
        }

        await self.websocket.send(
            json.dumps(request)
        )

        response = (
            await self.websocket.recv()
        )

        return json.loads(response)

    async def listen(self):

        if not self.websocket:

            raise RuntimeError(
                "WebSocket is not connected"
            )

        async for message in self.websocket:

            yield json.loads(message)