from decimal import Decimal

from app.risk.engine import RiskEngine


def test_buy_high_confidence_passes():
    engine = RiskEngine()

    result = engine.evaluate(
        decision="BUY",
        confidence=Decimal("85"),
        risk_level="MEDIUM",
        liquidity_usd=Decimal("20000"),
    )

    assert result.approved is True
    assert result.decision == "APPROVE"
    assert result.position_size_usd == Decimal("25")
    assert result.risk_level == "MEDIUM"
    assert result.reasons == []


def test_low_confidence_rejected():
    engine = RiskEngine()

    result = engine.evaluate(
        decision="BUY",
        confidence=Decimal("60"),
        risk_level="MEDIUM",
        liquidity_usd=Decimal("20000"),
    )

    assert result.approved is False
    assert result.decision == "REJECT"
    assert result.position_size_usd == Decimal("0")
    assert "AI_CONFIDENCE_TOO_LOW" in result.reasons


def test_high_risk_rejected():
    engine = RiskEngine()

    result = engine.evaluate(
        decision="BUY",
        confidence=Decimal("85"),
        risk_level="HIGH",
        liquidity_usd=Decimal("20000"),
    )

    assert result.approved is False
    assert result.decision == "REJECT"
    assert result.position_size_usd == Decimal("0")
    assert "RISK_LEVEL_TOO_HIGH" in result.reasons


def test_low_liquidity_rejected():
    engine = RiskEngine()

    result = engine.evaluate(
        decision="BUY",
        confidence=Decimal("85"),
        risk_level="MEDIUM",
        liquidity_usd=Decimal("5000"),
    )

    assert result.approved is False
    assert result.decision == "REJECT"
    assert result.position_size_usd == Decimal("0")
    assert "LIQUIDITY_TOO_LOW" in result.reasons


def test_watch_rejected():
    engine = RiskEngine()

    result = engine.evaluate(
        decision="WATCH",
        confidence=Decimal("90"),
        risk_level="LOW",
        liquidity_usd=Decimal("20000"),
    )

    assert result.approved is False
    assert result.decision == "REJECT"
    assert result.position_size_usd == Decimal("0")
    assert "AI_DECISION_NOT_BUY" in result.reasons


def test_reject_rejected():
    engine = RiskEngine()

    result = engine.evaluate(
        decision="REJECT",
        confidence=Decimal("95"),
        risk_level="LOW",
        liquidity_usd=Decimal("20000"),
    )

    assert result.approved is False
    assert result.decision == "REJECT"
    assert result.position_size_usd == Decimal("0")
    assert "AI_DECISION_NOT_BUY" in result.reasons


if __name__ == "__main__":
    print("RISK ENGINE TEST PASSED")