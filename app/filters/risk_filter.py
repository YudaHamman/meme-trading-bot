from typing import Any

from app.config import (
    MAX_PRICE_CHANGE_5M,
    MAX_PRICE_CHANGE_1H,
)


def check_risk(
    pair: dict[str, Any],
) -> dict[str, Any]:

    price_change = (
        pair.get("priceChange") or {}
    )

    try:
        change_5m = float(
            price_change.get("m5") or 0
        )
    except (TypeError, ValueError):
        change_5m = 0.0

    try:
        change_1h = float(
            price_change.get("h1") or 0
        )
    except (TypeError, ValueError):
        change_1h = 0.0

    extreme_5m = (
        change_5m
        > MAX_PRICE_CHANGE_5M
    )

    extreme_1h = (
        change_1h
        > MAX_PRICE_CHANGE_1H
    )

    passed = not (
        extreme_5m
        or extreme_1h
    )

    reasons = []

    if extreme_5m:
        reasons.append(
            "Price spike 5M terlalu tinggi"
        )

    if extreme_1h:
        reasons.append(
            "Price spike 1H terlalu tinggi"
        )

    if not reasons:
        reasons.append(
            "Tidak ada price spike ekstrem"
        )

    return {
        "passed": passed,
        "change_5m": change_5m,
        "change_1h": change_1h,
        "extreme_5m": extreme_5m,
        "extreme_1h": extreme_1h,
        "reasons": reasons,
    }