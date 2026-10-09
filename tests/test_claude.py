import asyncio

from app.ai.claude import ClaudeClient


async def main():
    claude = ClaudeClient()

    try:
        result = await claude.ask(
            system_prompt="You are a trading market analysis assistant.",
            user_prompt="Reply with exactly: CLAUDE CONNECTION OK",
        )

        print("\nCLAUDE RESPONSE:")
        print(result)

    finally:
        await claude.close()


if __name__ == "__main__":
    asyncio.run(main())