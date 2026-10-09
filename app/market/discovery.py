from datetime import datetime, timezone

from app.core.logger import logger
from app.market.models import TokenMarket


class TokenDiscoveryEngine:

    def __init__(self):
        self.known_tokens: set[str] = set()

    def discover(
        self,
        tokens: list[TokenMarket],
        source: str,
    ) -> list[TokenMarket]:

        new_tokens = []

        for token in tokens:

            # Validate mint address
            if not token.address:
                continue

            # Validate token metadata
            if not token.symbol:
                continue

            if not token.name:
                continue

            # Deduplicate
            if token.address in self.known_tokens:
                continue

            # Register token
            self.known_tokens.add(
                token.address
            )

            # Add discovery metadata
            token.source = source

            if token.launch_timestamp is None:
                token.launch_timestamp = (
                    datetime.now(timezone.utc)
                )

            new_tokens.append(token)

            logger.info(
                "NEW TOKEN | %s | %s | %s",
                token.symbol,
                token.name,
                token.address,
            )

        return new_tokens