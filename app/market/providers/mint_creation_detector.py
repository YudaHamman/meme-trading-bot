from typing import Any
import base64


PUMP_PROGRAM_ID = (
    "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
)


# create_v2 discriminator
CREATE_V2_DISCRIMINATOR = bytes([
    209,
    112,
    49,
    197,
    2,
    253,
    214,
    148,
])


class MintCreationDetector:

    @staticmethod
    def is_create_instruction(
        instruction: dict[str, Any],
    ) -> bool:

        if not instruction:
            return False

        if instruction.get("programId") != PUMP_PROGRAM_ID:
            return False

        data = instruction.get("data")

        if not data:
            return False

        try:

            decoded = base64.b64decode(data)

        except Exception:

            return False

        return decoded.startswith(
            CREATE_V2_DISCRIMINATOR
        )

    @staticmethod
    def find_create_instruction(
        transaction: dict[str, Any],
    ) -> dict[str, Any] | None:

        if not transaction:
            return None

        message = (
            transaction
            .get("transaction", {})
            .get("message", {})
        )

        instructions = message.get(
            "instructions",
            []
        )

        for instruction in instructions:

            if MintCreationDetector.is_create_instruction(
                instruction
            ):
                return instruction

        return None