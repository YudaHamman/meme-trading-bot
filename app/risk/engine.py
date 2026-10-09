from decimal import Decimal

from app.ai.models import AIAnalysis
from app.market.models import TokenMarket
from app.risk.models import RiskConfig, RiskDecision


class RiskEngine:
    def __init__(self, config: RiskConfig | None = None):
        self.config = config or RiskConfig()

    def evaluate(
        self,
        *,
        decision: str | None = None,
        confidence: Decimal | None = None,
        risk_level: str | None = None,
        liquidity_usd: Decimal | None = None,
        token: TokenMarket | None = None,
        ai_analysis: AIAnalysis | None = None,
    ) -> RiskDecision:
        if ai_analysis is not None:
            decision = ai_analysis.decision
            confidence = ai_analysis.confidence
            risk_level = ai_analysis.risk_level

        if token is not None:
            liquidity_usd = token.liquidity_usd

        if (
            decision is None
            or confidence is None
            or risk_level is None
            or liquidity_usd is None
        ):
            raise ValueError(
                "RiskEngine.evaluate requires decision, confidence, "
                "risk_level, and liquidity_usd"
            )

        reasons: list[str] = []

        # AI decision harus BUY
        if decision != "BUY":
            reasons.append("AI_DECISION_NOT_BUY")

        # Confidence minimum
        if confidence < self.config.min_confidence:
            reasons.append("AI_CONFIDENCE_TOO_LOW")

        # Risk level maksimum
        risk_order = {
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3,
        }

        current_risk = risk_order.get(risk_level, 99)
        maximum_risk = risk_order.get(
            self.config.max_risk_level,
            2,
        )

        if current_risk > maximum_risk:
            reasons.append("RISK_LEVEL_TOO_HIGH")

        # Minimum liquidity
        if liquidity_usd < self.config.min_liquidity_usd:
            reasons.append("LIQUIDITY_TOO_LOW")

        approved = len(reasons) == 0

        return RiskDecision(
            approved=approved,
            decision="APPROVE" if approved else "REJECT",
            position_size_usd=(
                self.config.max_position_usd
                if approved
                else Decimal("0")
            ),
            risk_level=risk_level,
            reasons=reasons,
        )
