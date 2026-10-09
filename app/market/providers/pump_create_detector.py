from typing import Any


PUMP_PROGRAM_ID = (
    "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
)


CREATE_INSTRUCTIONS = {
    "Create",
    "CreateV2",
}


class PumpCreateDetector:

    @staticmethod
    def extract_pump_top_level_instructions(
        logs: list[str],
    ) -> list[str]:

        instructions: list[str] = []

        waiting_for_instruction = False

        for log in logs:

            # Pump.fun starts a TOP-LEVEL instruction.
            if log == (
                f"Program {PUMP_PROGRAM_ID} invoke [1]"
            ):
                waiting_for_instruction = True
                continue

            # The first instruction log after Pump.fun
            # invoke [1] belongs to that Pump.fun instruction.
            if waiting_for_instruction:

                prefix = "Program log: Instruction: "

                if log.startswith(prefix):

                    instruction = log[
                        len(prefix):
                    ].strip()

                    instructions.append(
                        instruction
                    )

                    waiting_for_instruction = False

                    continue

                # If another program appears before an
                # instruction log, stop waiting.
                if log.startswith("Program "):
                    waiting_for_instruction = False

        return instructions

    @staticmethod
    def get_create_instruction(
        event: dict[str, Any],
    ) -> str | None:

        params = event.get("params", {})
        result = params.get("result", {})
        value = result.get("value", {})

        if value.get("err") is not None:
            return None

        logs = value.get("logs", [])

        if not logs:
            return None

        instructions = (
            PumpCreateDetector
            .extract_pump_top_level_instructions(
                logs
            )
        )

        for instruction in instructions:

            if instruction in CREATE_INSTRUCTIONS:
                return instruction

        return None

    @staticmethod
    def is_create_event(
        event: dict[str, Any],
    ) -> bool:

        instruction = (
            PumpCreateDetector
            .get_create_instruction(
                event
            )
        )

        return instruction is not None