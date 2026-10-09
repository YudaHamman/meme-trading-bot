from typing import Any


class PumpEventParser:

    @staticmethod
    def parse(event: dict[str, Any]) -> dict[str, Any] | None:

        params = event.get("params", {})
        result = params.get("result", {})
        value = result.get("value", {})

        signature = value.get("signature")
        logs = value.get("logs", [])
        err = value.get("err")

        if not signature:
            return None

        joined_logs = "\n".join(logs)

        is_pump_event = (
            "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
            in joined_logs
        )

        if not is_pump_event:
            return None

        instruction = None

        if "BondingCurveV3" in joined_logs:
            instruction = "BondingCurveV3"
        elif "BuyExactQuoteInV2" in joined_logs:
            instruction = "BuyExactQuoteInV2"
        elif "Sell" in joined_logs:
            instruction = "Sell"

        return {
            "signature": signature,
            "slot": result.get("context", {}).get("slot"),
            "success": err is None,
            "error": err,
            "instruction": instruction,
        }