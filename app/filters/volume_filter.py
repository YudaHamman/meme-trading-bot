from typing import Any

from app.config import (
    MIN_VOLUME_5M_USD,
    MIN_VOLUME_1H_USD,
)


def check_volume(
    pair: dict[str, Any],
) -> dict[str, Any]:

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

    passed_5m = (
        volume_5m
        >= MIN_VOLUME_5M_USD
    )

    passed_1h = (
        volume_1h
        >= MIN_VOLUME_1H_USD
    )

    return {
        "passed": (
            passed_5m
            and passed_1h
        ),
        "passed_5m": passed_5m,
        "passed_1h": passed_1h,
        "volume_5m": volume_5m,
        "volume_1h": volume_1h,
    }