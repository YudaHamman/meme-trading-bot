from abc import ABC, abstractmethod

from app.market.models import TokenMarket


class MarketDataProvider(ABC):

    @abstractmethod
    async def get_token(self, address: str) -> TokenMarket | None:
        pass

    @abstractmethod
    async def search_tokens(self, query: str) -> list[TokenMarket]:
        pass