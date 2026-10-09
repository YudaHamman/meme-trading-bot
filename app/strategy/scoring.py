from typing import Any

from app.config import (
    MIN_LIQUIDITY_USD,
    MIN_VOLUME_5M_USD,
    MIN_VOLUME_1H_USD,
    MIN_BUYS_5M,
    MIN_BUY_RATIO,
    MIN_PRICE_CHANGE_5M,
    MIN_PRICE_CHANGE_1H,
    BUY_SCORE,
    WATCH_SCORE,
)


def calculate_score(
    pair: dict[str, Any],
) -> dict[str, Any]:

    score = 0
    reasons = []

    # ==============================
    # LIQUIDITY — 20 POINT
    # ==============================

    liquidity = pair.get(
        "liquidity"
    ) or {}

    try:
        liquidity_usd = float(
            liquidity.get("usd") or 0
        )
    except (TypeError, ValueError):
        liquidity_usd = 0.0

    if liquidity_usd >= MIN_LIQUIDITY_USD:
        score += 20
        reasons.append(
            "Liquidity OK"
        )
    else:
        reasons.append(
            "Liquidity rendah"
        )

    # ==============================
    # VOLUME — 30 POINT
    # ==============================

    volume = pair.get("volume") or {}

    try:
        volume_5m = float(
            volume.get("m5") or 0
        )
    except (TypeError, ValueError):
        volume_5m = 0.0

    try:
        volume_1h = float(
            volume.get("h1") or 0
        )
    except (TypeError, ValueError):
        volume_1h = 0.0

    if volume_5m >= MIN_VOLUME_5M_USD:
        score += 15
        reasons.append(
            "Volume 5M OK"
        )
    else:
        reasons.append(
            "Volume 5M rendah"
        )

    if volume_1h >= MIN_VOLUME_1H_USD:
        score += 15
        reasons.append(
            "Volume 1H OK"
        )
    else:
        reasons.append(
            "Volume 1H rendah"
        )

    # ==============================
    # TRANSACTIONS — 25 POINT
    # ==============================

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

    total_tx = buys + sells

    if total_tx > 0:
        buy_ratio = (
            buys / total_tx
        )
    else:
        buy_ratio = 0.0

    if buys >= MIN_BUYS_5M:
        score += 10
        reasons.append(
            "Buyer aktif"
        )
    else:
        reasons.append(
            "Buyer sedikit"
        )

    if buy_ratio >= MIN_BUY_RATIO:
        score += 15
        reasons.append(
            "Buy pressure kuat"
        )
    else:
        reasons.append(
            "Buy pressure lemah"
        )

    # ==============================
    # MOMENTUM — 25 POINT
    # ==============================

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

    if change_5m >= MIN_PRICE_CHANGE_5M:
        score += 10
        reasons.append(
            "Momentum 5M positif"
        )
    else:
        reasons.append(
            "Momentum 5M lemah"
        )

    if change_1h >= MIN_PRICE_CHANGE_1H:
        score += 15
        reasons.append(
            "Trend 1H positif"
        )
    else:
        reasons.append(
            "Trend 1H lemah"
        )

    # ==============================
    # SIGNAL
    # ==============================

    if score >= BUY_SCORE:
        signal = "BUY"

    elif score >= WATCH_SCORE:
        signal = "WATCH"

    else:
        signal = "SKIP"

    return {
        "score": score,
        "signal": signal,
        "reasons": reasons,

        "liquidity": liquidity_usd,

        "volume_5m": volume_5m,
        "volume_1h": volume_1h,

        "buys": buys,
        "sells": sells,
        "total_transactions": total_tx,
        "buy_ratio": buy_ratio,

        "change_5m": change_5m,
        "change_1h": change_1h,
    }