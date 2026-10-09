import asyncio

from app.market.providers.dexscreener import (
    DexScreenerProvider,
)
from app.market.scoring.engine import (
    ScoringEngine,
)
from app.market.scoring.ranking import (
    RankingEngine,
)


TOKENS = [
    "DtLQnXRu5FM2Rm3dw7RJd8BbH6xc2faY4W6Whgz8pump",
]


async def main():

    provider = DexScreenerProvider()
    scoring = ScoringEngine()

    candidates = []

    print()
    print("GETTING TOKEN MARKET DATA...")
    print()

    for mint in TOKENS:

        print(
            "CHECKING:",
            mint
        )

        market = await provider.get_market(
            mint
        )

        if not market:

            print(
                "MARKET NOT FOUND"
            )

            continue

        candidate = scoring.calculate(
            market
        )

        candidates.append(
            candidate
        )

        print(
            "TOKEN:",
            market.symbol
        )

        print(
            "SCORE:",
            candidate.score
        )

        print()

    print(
        "TOTAL CANDIDATES:",
        len(candidates)
    )

    print()
    print("RANKING...")

    ranked = RankingEngine.rank(
        candidates,
        limit=10,
    )

    print()
    print("RANKED TOKENS")
    print(
        "=============================="
    )

    for index, candidate in enumerate(
        ranked,
        start=1,
    ):

        print(
            f"#{index}",
            candidate.token.symbol,
            "→",
            candidate.score,
        )

    print()
    print("TEST PASSED")


if __name__ == "__main__":

    asyncio.run(
        main()
    )