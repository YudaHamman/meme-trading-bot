from decimal import Decimal

from app.market.models import TokenMarket


class MarketAnalysis:

    def __init__(
        self,
        momentum_score: Decimal,
        volume_score: Decimal,
        pressure_score: Decimal,
        liquidity_score: Decimal,
        overall_score: Decimal,
    ):
        self.momentum_score = momentum_score
        self.volume_score = volume_score
        self.pressure_score = pressure_score
        self.liquidity_score = liquidity_score
        self.overall_score = overall_score


class MarketAnalysisEngine:

    @staticmethod
    def clamp(value: Decimal) -> Decimal:

        if value < Decimal("0"):
            return Decimal("0")

        if value > Decimal("100"):
            return Decimal("100")

        return value

    def analyze(self, token: TokenMarket) -> MarketAnalysis:

        momentum = self._momentum_score(token)

        volume = self._volume_score(token)

        pressure = self._pressure_score(token)

        liquidity = self._liquidity_score(token)

        overall = (
            momentum * Decimal("0.30")
            + volume * Decimal("0.25")
            + pressure * Decimal("0.25")
            + liquidity * Decimal("0.20")
        )

        return MarketAnalysis(
            momentum_score=self.clamp(momentum),
            volume_score=self.clamp(volume),
            pressure_score=self.clamp(pressure),
            liquidity_score=self.clamp(liquidity),
            overall_score=self.clamp(overall),
        )

    def _momentum_score(
        self,
        token: TokenMarket,
    ) -> Decimal:

        change = token.price_change_5m

        if change >= Decimal("15"):
            return Decimal("100")

        if change >= Decimal("10"):
            return Decimal("85")

        if change >= Decimal("5"):
            return Decimal("70")

        if change > Decimal("0"):
            return Decimal("55")

        return Decimal("20")

    def _volume_score(
        self,
        token: TokenMarket,
    ) -> Decimal:

        volume = token.volume_5m_usd

        if volume >= Decimal("100000"):
            return Decimal("100")

        if volume >= Decimal("50000"):
            return Decimal("90")

        if volume >= Decimal("20000"):
            return Decimal("75")

        if volume >= Decimal("5000"):
            return Decimal("60")

        return Decimal("20")

    def _pressure_score(
        self,
        token: TokenMarket,
    ) -> Decimal:

        total = token.buys_5m + token.sells_5m

        if total == 0:
            return Decimal("0")

        buy_ratio = (
            Decimal(token.buys_5m)
            / Decimal(total)
        )

        if buy_ratio >= Decimal("0.80"):
            return Decimal("100")

        if buy_ratio >= Decimal("0.70"):
            return Decimal("85")

        if buy_ratio >= Decimal("0.60"):
            return Decimal("70")

        if buy_ratio >= Decimal("0.50"):
            return Decimal("55")

        return Decimal("25")

    def _liquidity_score(
        self,
        token: TokenMarket,
    ) -> Decimal:

        liquidity = token.liquidity_usd

        if liquidity >= Decimal("500000"):
            return Decimal("100")

        if liquidity >= Decimal("250000"):
            return Decimal("90")

        if liquidity >= Decimal("100000"):
            return Decimal("80")

        if liquidity >= Decimal("50000"):
            return Decimal("65")

        if liquidity >= Decimal("10000"):
            return Decimal("50")

        return Decimal("10")