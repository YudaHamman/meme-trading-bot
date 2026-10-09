from datetime import datetime, timezone
from decimal import Decimal

from app.market.models import TokenMarket
from app.market.scoring.filter import CandidateFilter


def create_token(
    *,
    liquidity: Decimal = Decimal("20000"),
    volume_5m: Decimal = Decimal("1229.3"),
    buys: int = 20,
    sells: int = 22,
    price_change_5m: Decimal = Decimal("0"),
):
    return TokenMarket(
        address="TEST",
        symbol="TEST",
        name="Test Token",
        price_usd=Decimal("0.000001"),
        market_cap_usd=Decimal("0"),
        liquidity_usd=liquidity,
        volume_5m_usd=volume_5m,
        volume_1h_usd=volume_5m,
        volume_24h_usd=volume_5m,
        price_change_5m=price_change_5m,
        price_change_1h=Decimal("0"),
        price_change_24h=Decimal("0"),
        buys_5m=buys,
        sells_5m=sells,
        pair_address="TEST_PAIR",
        dex="pumpfun",
        updated_at=datetime.now(timezone.utc),
        source="test",
    )


def test_valid_candidate():

    candidate_filter = CandidateFilter()

    token = create_token()

    passed, reasons = candidate_filter.check(
        token,
        score=Decimal("50"),
    )

    assert passed is True
    assert reasons == []


def test_zero_liquidity_rejected():

    candidate_filter = CandidateFilter()

    token = create_token(
        liquidity=Decimal("0"),
    )

    passed, reasons = candidate_filter.check(
        token,
        score=Decimal("50"),
    )

    assert passed is False
    assert "LIQUIDITY_TOO_LOW" in reasons


def test_low_volume_rejected():

    candidate_filter = CandidateFilter()

    token = create_token(
        volume_5m=Decimal("100"),
    )

    passed, reasons = candidate_filter.check(
        token,
        score=Decimal("50"),
    )

    assert passed is False
    assert "VOLUME_5M_TOO_LOW" in reasons


def test_low_transactions_rejected():

    candidate_filter = CandidateFilter()

    token = create_token(
        buys=3,
        sells=3,
    )

    passed, reasons = candidate_filter.check(
        token,
        score=Decimal("50"),
    )

    assert passed is False
    assert "TRANSACTIONS_5M_TOO_LOW" in reasons


def test_low_buy_pressure_rejected():

    candidate_filter = CandidateFilter()

    token = create_token(
        buys=4,
        sells=20,
    )

    passed, reasons = candidate_filter.check(
        token,
        score=Decimal("50"),
    )

    assert passed is False
    assert "BUY_PRESSURE_TOO_LOW" in reasons


def test_extreme_buy_pressure_rejected():

    candidate_filter = CandidateFilter()

    token = create_token(
        buys=95,
        sells=5,
    )

    passed, reasons = candidate_filter.check(
        token,
        score=Decimal("50"),
    )

    assert passed is False
    assert (
        "BUY_PRESSURE_SUSPICIOUSLY_HIGH"
        in reasons
    )


def test_low_score_rejected():

    candidate_filter = CandidateFilter()

    token = create_token()

    passed, reasons = candidate_filter.check(
        token,
        score=Decimal("10"),
    )

    assert passed is False
    assert "SCORE_TOO_LOW" in reasons


def test_extreme_price_drop_rejected():

    candidate_filter = CandidateFilter()

    token = create_token(
        price_change_5m=Decimal("-60"),
    )

    passed, reasons = candidate_filter.check(
        token,
        score=Decimal("50"),
    )

    assert passed is False
    assert (
        "EXTREME_PRICE_DROP_5M"
        in reasons
    )


if __name__ == "__main__":
    print("CANDIDATE FILTER TEST PASSED")