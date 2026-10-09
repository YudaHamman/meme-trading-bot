from typing import Any

from app.config import MIN_LIQUIDITY_USD


def check_liquidity(
    pair: dict[str, Any],
) -> dict[str, Any]:

    liquidity = pair.get("liquidity") or {}

    try:
        liquidity_usd = float(
            liquidity.get("usd") or 0
        )
    except (TypeError, ValueError):
        liquidity_usd = 0.0

    passed = (
        liquidity_usd
        >= MIN_LIQUIDITY_USD
    )

    return {
        "passed": passed,
        "liquidity": liquidity_usd,
        "minimum": MIN_LIQUIDITY_USD,
    }