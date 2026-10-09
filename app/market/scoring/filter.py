from decimal import Decimal

from app.market.models import TokenMarket


class CandidateFilter:

    def __init__(
        self,
        min_volume_5m: Decimal = Decimal("500"),
        min_transactions_5m: int = 10,
        min_buy_ratio: Decimal = Decimal("0.45"),
        max_buy_ratio: Decimal = Decimal("0.90"),
        min_liquidity_usd: Decimal = Decimal("1"),
        min_score: Decimal = Decimal("20"),
        max_price_drop_5m: Decimal = Decimal("-50"),
    ):

        self.min_volume_5m = min_volume_5m
        self.min_transactions_5m = min_transactions_5m
        self.min_buy_ratio = min_buy_ratio
        self.max_buy_ratio = max_buy_ratio
        self.min_liquidity_usd = min_liquidity_usd
        self.min_score = min_score
        self.max_price_drop_5m = max_price_drop_5m

    def check(
        self,
        token: TokenMarket,
        score: Decimal | None = None,
    ) -> tuple[bool, list[str]]:

        reasons: list[str] = []

        total_transactions = (
            token.buys_5m
            + token.sells_5m
        )

        buy_ratio = Decimal("0")

        if total_transactions > 0:

            buy_ratio = (
                Decimal(token.buys_5m)
                / Decimal(total_transactions)
            )

        # =====================================
        # VOLUME
        # =====================================

        if token.volume_5m_usd < self.min_volume_5m:

            reasons.append(
                "VOLUME_5M_TOO_LOW"
            )

        # =====================================
        # TRANSACTIONS
        # =====================================

        if total_transactions < self.min_transactions_5m:

            reasons.append(
                "TRANSACTIONS_5M_TOO_LOW"
            )

        # =====================================
        # BUY PRESSURE
        # =====================================

        if total_transactions > 0:

            if buy_ratio < self.min_buy_ratio:

                reasons.append(
                    "BUY_PRESSURE_TOO_LOW"
                )

            if buy_ratio > self.max_buy_ratio:

                reasons.append(
                    "BUY_PRESSURE_SUSPICIOUSLY_HIGH"
                )

        # =====================================
        # LIQUIDITY
        # =====================================

        if token.liquidity_usd < self.min_liquidity_usd:

            reasons.append(
                "LIQUIDITY_TOO_LOW"
            )

        # =====================================
        # SCORE
        # =====================================

        if score is not None:

            if score < self.min_score:

                reasons.append(
                    "SCORE_TOO_LOW"
                )

        # =====================================
        # PRICE DROP
        # =====================================

        if token.price_change_5m <= self.max_price_drop_5m:

            reasons.append(
                "EXTREME_PRICE_DROP_5M"
            )

        return (
            len(reasons) == 0,
            reasons,
        )

    def explain(
        self,
        token: TokenMarket,
        score: Decimal | None = None,
    ) -> dict:

        total_transactions = (
            token.buys_5m
            + token.sells_5m
        )

        buy_ratio = Decimal("0")

        if total_transactions > 0:

            buy_ratio = (
                Decimal(token.buys_5m)
                / Decimal(total_transactions)
            )

        return {
            "volume_5m": {
                "value": token.volume_5m_usd,
                "minimum": self.min_volume_5m,
                "passed": (
                    token.volume_5m_usd
                    >= self.min_volume_5m
                ),
            },

            "transactions_5m": {
                "value": total_transactions,
                "minimum": self.min_transactions_5m,
                "passed": (
                    total_transactions
                    >= self.min_transactions_5m
                ),
            },

            "buy_ratio": {
                "value": buy_ratio,
                "minimum": self.min_buy_ratio,
                "maximum": self.max_buy_ratio,
                "passed": (
                    total_transactions == 0
                    or (
                        buy_ratio
                        >= self.min_buy_ratio
                        and buy_ratio
                        <= self.max_buy_ratio
                    )
                ),
            },

            "liquidity_usd": {
                "value": token.liquidity_usd,
                "minimum": self.min_liquidity_usd,
                "passed": (
                    token.liquidity_usd
                    >= self.min_liquidity_usd
                ),
            },

            "score": {
                "value": score,
                "minimum": self.min_score,
                "passed": (
                    score is None
                    or score >= self.min_score
                ),
            },

            "price_change_5m": {
                "value": token.price_change_5m,
                "minimum": self.max_price_drop_5m,
                "passed": (
                    token.price_change_5m
                    > self.max_price_drop_5m
                ),
            },
        }