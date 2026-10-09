from typing import Any

from app.config import (
    MIN_BUYS_5M,
    MIN_TOTAL_TX_5M,
    MIN_BUY_RATIO,
)


def check_transactions(
    pair: dict[str, Any],
) -> dict[str, Any]:

    txns = pair.get("txns") or {}
    tx_5m = txns.get("m5") or {}

    try:
        buys = int(
            tx_5m.get("buys") or 0
        )
    except (TypeError, ValueError):
        buys = 0

    try:
        sells = int(
            tx_5m.get("sells") or 0
        )
    except (TypeError, ValueError):
        sells = 0

    total_transactions = (
        buys + sells
    )

    if total_transactions > 0:
        buy_ratio = (
            buys / total_transactions
        )
    else:
        buy_ratio = 0.0

    passed_buys = (
        buys >= MIN_BUYS_5M
    )

    passed_total = (
        total_transactions
        >= MIN_TOTAL_TX_5M
    )

    passed_ratio = (
        buy_ratio >= MIN_BUY_RATIO
    )

    return {
        "passed": (
            passed_buys
            and passed_total
            and passed_ratio
        ),
        "passed_buys": passed_buys,
        "passed_total": passed_total,
        "passed_ratio": passed_ratio,
        "buys": buys,
        "sells": sells,
        "total_transactions": total_transactions,
        "buy_ratio": buy_ratio,
    }