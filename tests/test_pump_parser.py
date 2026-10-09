from app.market.providers.pump_parser import PumpEventParser


event = {
    "params": {
        "result": {
            "context": {
                "slot": 443994047
            },
            "value": {
                "signature": "TEST_SIGNATURE",
                "err": None,
                "logs": [
                    "Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P invoke [3]",
                    "Program log: Instruction: BondingCurveV3",
                    "Program log: Instruction: BuyExactQuoteInV2",
                    "Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P success",
                ],
            },
        }
    }
}


result = PumpEventParser.parse(event)

print(result)

assert result is not None
assert result["signature"] == "TEST_SIGNATURE"
assert result["slot"] == 443994047
assert result["success"] is True
assert result["instruction"] == "BondingCurveV3"

print("PUMP EVENT PARSER OK")