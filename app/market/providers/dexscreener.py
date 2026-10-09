from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

import httpx

from app.market.models import TokenMarket


DEXSCREENER_TOKEN_URL = (
    "https://api.dexscreener.com/latest/dex/tokens/"
)

DEXSCREENER_SEARCH_URL = (
    "https://api.dexscreener.com/latest/dex/search"
)


class DexScreenerProvider:

    async def search(
        self,
        query: str,
    ) -> dict[str, Any]:

        async with httpx.AsyncClient(
            timeout=15
        ) as client:

            response = await client.get(
                DEXSCREENER_SEARCH_URL,
                params={
                    "q": query,
                },
            )

            response.raise_for_status()

            return response.json()

    async def search_tokens(
        self,
        query: str,
    ) -> list[TokenMarket]:

        data = await self.search(query)

        pairs = data.get("pairs") or []

        return [
            self.normalize_pair(pair)
            for pair in pairs
            if pair.get("chainId") == "solana"
        ]

    async def close(self) -> None:
        return None

    async def get_token_pairs(
        self,
        token_address: str,
    ) -> list[dict[str, Any]]:

        url = (
            f"{DEXSCREENER_TOKEN_URL}"
            f"{token_address}"
        )

        async with httpx.AsyncClient(
            timeout=15
        ) as client:

            response = await client.get(
                url
            )

            response.raise_for_status()

            data = response.json()

        pairs = data.get("pairs")

        if not pairs:
            return []

        return pairs

    @staticmethod
    def to_decimal(
        value: Any,
    ) -> Decimal:

        if value is None:
            return Decimal("0")

        try:
            return Decimal(str(value))
        except (
            InvalidOperation,
            ValueError,
            TypeError,
        ):
            return Decimal("0")

    @staticmethod
    def get_nested_value(
        data: dict[str, Any],
        parent: str,
        key: str,
    ) -> Any:

        section = data.get(parent) or {}

        return section.get(key)

    def normalize_pair(
        self,
        pair: dict[str, Any],
    ) -> TokenMarket:

        base_token = (
            pair.get("baseToken")
            or {}
        )

        quote_token = (
            pair.get("quoteToken")
            or {}
        )

        liquidity = (
            pair.get("liquidity")
            or {}
        )

        volume = (
            pair.get("volume")
            or {}
        )

        price_change = (
            pair.get("priceChange")
            or {}
        )

        txns = (
            pair.get("txns")
            or {}
        )

        txns_5m = (
            txns.get("m5")
            or {}
        )

        address = (
            base_token.get("address")
            or ""
        )

        symbol = (
            base_token.get("symbol")
            or ""
        )

        name = (
            base_token.get("name")
            or ""
        )

        return TokenMarket(
            address=address,

            symbol=symbol,

            name=name,

            price_usd=self.to_decimal(
                pair.get("priceUsd")
            ),

            market_cap_usd=self.to_decimal(
                pair.get("marketCap")
                or pair.get("fdv")
            ),

            liquidity_usd=self.to_decimal(
                liquidity.get("usd")
            ),

            volume_5m_usd=self.to_decimal(
                volume.get("m5")
            ),

            volume_1h_usd=self.to_decimal(
                volume.get("h1")
            ),

            volume_24h_usd=self.to_decimal(
                volume.get("h24")
            ),

            price_change_5m=self.to_decimal(
                price_change.get("m5")
            ),

            price_change_1h=self.to_decimal(
                price_change.get("h1")
            ),

            price_change_24h=self.to_decimal(
                price_change.get("h24")
            ),

            buys_5m=int(
                txns_5m.get("buys") or 0
            ),

            sells_5m=int(
                txns_5m.get("sells") or 0
            ),

            pair_address=pair.get(
                "pairAddress"
            ),

            dex=pair.get(
                "dexId"
            ),

            updated_at=datetime.now(
                timezone.utc
            ),

            source="dexscreener",
        )

    async def get_best_pair(
        self,
        token_address: str,
    ) -> dict[str, Any] | None:

        pairs = await self.get_token_pairs(
            token_address
        )

        if not pairs:
            return None

        solana_pairs = [
            pair
            for pair in pairs
            if pair.get("chainId") == "solana"
        ]

        if not solana_pairs:
            return None

        def liquidity_value(
            pair: dict[str, Any],
        ) -> Decimal:

            liquidity = (
                pair.get("liquidity")
                or {}
            )

            return self.to_decimal(
                liquidity.get("usd")
            )

        solana_pairs.sort(
            key=liquidity_value,
            reverse=True,
        )

        return solana_pairs[0]

    async def get_market(
        self,
        token_address: str,
    ) -> TokenMarket | None:

        pair = await self.get_best_pair(
            token_address
        )

        if not pair:
            return None

        return self.normalize_pair(
            pair
        )
