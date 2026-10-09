from decimal import Decimal

from app.market.models import TokenMarket


class CandidateScore:
    def __init__(
        self,
        token: TokenMarket,
        score: Decimal,
    ):
        self.token = token
        self.score = score


class ScoringEngine:

    def calculate(self, token: TokenMarket) -> CandidateScore:

        score = Decimal("0")

        # Liquidity
        if token.liquidity_usd >= Decimal("100000"):
            score += Decimal("25")
        elif token.liquidity_usd >= Decimal("50000"):
            score += Decimal("20")
        elif token.liquidity_usd >= Decimal("10000"):
            score += Decimal("10")

        # Volume
        if token.volume_5m_usd >= Decimal("50000"):
            score += Decimal("25")
        elif token.volume_5m_usd >= Decimal("20000"):
            score += Decimal("20")
        elif token.volume_5m_usd >= Decimal("5000"):
            score += Decimal("10")

        # Momentum
        if token.price_change_5m >= Decimal("10"):
            score += Decimal("20")
        elif token.price_change_5m >= Decimal("5"):
            score += Decimal("15")
        elif token.price_change_5m > Decimal("0"):
            score += Decimal("10")

        # Buy/Sell pressure
        total_transactions = token.buys_5m + token.sells_5m

        if total_transactions > 0:

            buy_ratio = (
                Decimal(token.buys_5m)
                / Decimal(total_transactions)
            )

            if buy_ratio >= Decimal("0.70"):
                score += Decimal("20")

            elif buy_ratio >= Decimal("0.60"):
                score += Decimal("15")

            elif buy_ratio >= Decimal("0.50"):
                score += Decimal("10")

        # Market cap
        if token.market_cap_usd > 0:
            liquidity_ratio = (
                token.liquidity_usd
                / token.market_cap_usd
            )

            if liquidity_ratio >= Decimal("0.10"):
                score += Decimal("10")

            elif liquidity_ratio >= Decimal("0.05"):
                score += Decimal("5")

        return CandidateScore(
            token=token,
            score=min(score, Decimal("100")),
        )