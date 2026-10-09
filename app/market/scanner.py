from decimal import Decimal

from app.core.logger import logger
from app.market.models import TokenMarket


class TokenScanner:

    def __init__(
        self,
        min_liquidity_usd: Decimal = Decimal("10000"),
        min_volume_5m_usd: Decimal = Decimal("5000"),
        min_buys_5m: int = 5,
    ):
        self.min_liquidity_usd = min_liquidity_usd
        self.min_volume_5m_usd = min_volume_5m_usd
        self.min_buys_5m = min_buys_5m

    def filter_candidates(
        self,
        tokens: list[TokenMarket],
    ) -> list[TokenMarket]:

        candidates = []

        for token in tokens:

            if token.liquidity_usd < self.min_liquidity_usd:
                continue

            if token.volume_5m_usd < self.min_volume_5m_usd:
                continue

            if token.buys_5m < self.min_buys_5m:
                continue

            candidates.append(token)

        logger.info(
            "Scanner: %d candidates from %d tokens",
            len(candidates),
            len(tokens),
        )

        return candidates