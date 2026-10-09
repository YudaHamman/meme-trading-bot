from decimal import Decimal

from app.market.models import TokenMarket
from app.market.analysis.engine import MarketAnalysisEngine
from app.market.scoring.engine import ScoringEngine


class MarketIntelligence:

    def __init__(self):
        self.scoring = ScoringEngine()
        self.analysis = MarketAnalysisEngine()

    def analyze(
        self,
        token: TokenMarket,
    ) -> dict:

        # =====================================
        # BUY PRESSURE
        # =====================================

        total_transactions = (
            token.buys_5m
            + token.sells_5m
        )

        if total_transactions > 0:

            buy_pressure = (
                Decimal(token.buys_5m)
                / Decimal(total_transactions)
                * Decimal("100")
            )

        else:

            buy_pressure = Decimal("0")

        # =====================================
        # MOMENTUM
        # =====================================

        if (
            token.price_change_5m
            >= Decimal("10")
        ):

            momentum = "STRONG_BULLISH"

        elif (
            token.price_change_5m
            >= Decimal("5")
        ):

            momentum = "BULLISH"

        elif (
            token.price_change_5m
            > Decimal("0")
        ):

            momentum = "WEAK_BULLISH"

        elif (
            token.price_change_5m
            <= Decimal("-10")
        ):

            momentum = "STRONG_BEARISH"

        elif (
            token.price_change_5m
            < Decimal("0")
        ):

            momentum = "BEARISH"

        else:

            momentum = "NEUTRAL"

        # =====================================
        # VOLUME STATUS
        # =====================================

        if (
            token.volume_5m_usd
            >= Decimal("10000")
        ):

            volume_status = "HIGH"

        elif (
            token.volume_5m_usd
            >= Decimal("5000")
        ):

            volume_status = "MODERATE"

        elif (
            token.volume_5m_usd
            >= Decimal("500")
        ):

            volume_status = "LOW"

        else:

            volume_status = "VERY_LOW"

        # =====================================
        # LIQUIDITY STATUS
        # =====================================

        if (
            token.liquidity_usd
            >= Decimal("100000")
        ):

            liquidity_status = "HIGH"

        elif (
            token.liquidity_usd
            >= Decimal("50000")
        ):

            liquidity_status = "MODERATE"

        elif (
            token.liquidity_usd
            > Decimal("0")
        ):

            liquidity_status = "LOW"

        else:

            liquidity_status = "UNKNOWN"

        # =====================================
        # BUY PRESSURE STATUS
        # =====================================

        if buy_pressure >= Decimal("70"):

            buy_pressure_status = "VERY_STRONG"

        elif buy_pressure >= Decimal("60"):

            buy_pressure_status = "STRONG"

        elif buy_pressure >= Decimal("50"):

            buy_pressure_status = "POSITIVE"

        elif buy_pressure >= Decimal("40"):

            buy_pressure_status = "WEAK"

        else:

            buy_pressure_status = "NEGATIVE"

        # =====================================
        # RED FLAGS
        # =====================================

        red_flags: list[str] = []

        if token.liquidity_usd <= 0:

            red_flags.append(
                "NO_LIQUIDITY_DATA"
            )

        if (
            token.volume_5m_usd
            < Decimal("500")
        ):

            red_flags.append(
                "VERY_LOW_VOLUME"
            )

        if total_transactions < 10:

            red_flags.append(
                "LOW_TRANSACTION_ACTIVITY"
            )

        if buy_pressure > Decimal("90"):

            red_flags.append(
                "EXTREME_BUY_PRESSURE"
            )

        if buy_pressure < Decimal("40"):

            red_flags.append(
                "SELL_PRESSURE"
            )

        # =====================================
        # RESULT
        # =====================================

        return {
            "momentum": momentum,

            "buy_pressure": buy_pressure,

            "buy_pressure_status": (
                buy_pressure_status
            ),

            "volume_status": volume_status,

            "liquidity_status": (
                liquidity_status
            ),

            "total_transactions_5m": (
                total_transactions
            ),

            "red_flags": red_flags,
        }

    def analyze_tokens(
        self,
        tokens: list[TokenMarket],
        limit: int | None = None,
    ) -> list[dict]:
        results = []

        for token in tokens:
            candidate = self.scoring.calculate(token)
            analysis = self.analysis.analyze(token)

            results.append(
                {
                    "token": token,
                    "score": candidate.score,
                    "analysis": analysis,
                    "intelligence": self.analyze(token),
                }
            )

        results.sort(
            key=lambda result: result["score"],
            reverse=True,
        )

        if limit is not None:
            return results[:limit]

        return results
