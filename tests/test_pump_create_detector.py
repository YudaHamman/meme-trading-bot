from app.market.providers.pump_create_detector import (
    PumpCreateDetector,
)


def main():

    logs = [
        "Program ComputeBudget111111111111111111111111111111 invoke [1]",
        "Program ComputeBudget111111111111111111111111111111 success",

        "Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P invoke [1]",
        "Program log: Instruction: Create",

        "Program 11111111111111111111111111111111 invoke [2]",
        "Program 11111111111111111111111111111111 success",

        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]",
        "Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success",

        "Program ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL invoke [2]",
        "Program log: Create",

        "Program metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s invoke [2]",
        "Program log: IX: Create Metadata Accounts v3",

        "Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P success",

        "Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P invoke [1]",
        "Program log: Instruction: ExtendAccount",

        "Program 11111111111111111111111111111111 invoke [2]",
        "Program 11111111111111111111111111111111 success",

        "Program 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P success",
    ]

    event = {
        "params": {
            "result": {
                "value": {
                    "err": None,
                    "logs": logs,
                }
            }
        }
    }

    instructions = (
        PumpCreateDetector
        .extract_pump_top_level_instructions(
            logs
        )
    )

    print()
    print("PUMP TOP-LEVEL INSTRUCTIONS:")
    print(instructions)

    create_instruction = (
        PumpCreateDetector
        .get_create_instruction(
            event
        )
    )

    print()
    print("CREATE INSTRUCTION:")
    print(create_instruction)

    print()
    print("IS CREATE:")
    print(
        PumpCreateDetector.is_create_event(
            event
        )
    )

    print()

    assert instructions == [
        "Create",
        "ExtendAccount",
    ]

    assert create_instruction == "Create"

    assert (
        PumpCreateDetector.is_create_event(
            event
        )
        is True
    )

    print("TEST PASSED")


if __name__ == "__main__":
    main()