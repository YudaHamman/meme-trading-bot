import httpx

from app.core.logger import logger


class MarketDataClient:

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

        self.client = httpx.AsyncClient(
            timeout=10.0
        )

    async def close(self) -> None:
        await self.client.aclose()

    async def get(
        self,
        endpoint: str,
        params: dict | None = None,
    ) -> dict:

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        logger.debug("GET %s", url)

        response = await self.client.get(
            url,
            params=params,
        )

        response.raise_for_status()

        return response.json()