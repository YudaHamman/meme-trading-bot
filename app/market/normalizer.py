from datetime import datetime, timezone
from decimal import Decimal

from app.market.models import TokenMarket


class MarketNormalizer:

    @staticmethod
    def decimal(value) -> Decimal:
        if value is None:
            return Decimal("0")

        try:
            return Decimal(str(value))
        except (ValueError, TypeError):
            return Decimal("0")

    @classmethod
    def from_dexscreener(cls, pair: dict) -> TokenMarket:

        base_token = pair.get("baseToken", {})
        txns = pair.get("txns", {})
        volume = pair.get("volume", {})
        price_change = pair.get("priceChange", {})

        txns_5m = txns.get("m5", {})

        return TokenMarket(
            address=base_token.get("address", ""),
            symbol=base_token.get("symbol", ""),
            name=base_token.get("name", ""),

            price_usd=cls.decimal(pair.get("priceUsd")),

            market_cap_usd=cls.decimal(
                pair.get("marketCap")
            ),

            liquidity_usd=cls.decimal(
                pair.get("liquidity", {}).get("usd")
            ),

            volume_5m_usd=cls.decimal(
                volume.get("m5")
            ),

            volume_1h_usd=cls.decimal(
                volume.get("h1")
            ),

            volume_24h_usd=cls.decimal(
                volume.get("h24")
            ),

            price_change_5m=cls.decimal(
                price_change.get("m5")
            ),

            price_change_1h=cls.decimal(
                price_change.get("h1")
            ),

            price_change_24h=cls.decimal(
                price_change.get("h24")
            ),

            buys_5m=int(txns_5m.get("buys", 0)),
            sells_5m=int(txns_5m.get("sells", 0)),

            pair_address=pair.get("pairAddress"),
            dex=pair.get("dexId"),

            updated_at=datetime.now(timezone.utc),
        )