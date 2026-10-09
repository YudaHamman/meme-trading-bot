from datetime import datetime, timezone
from decimal import Decimal

from app.market.models import TokenMarket
from app.market.scoring.engine import CandidateScore
from app.market.scoring.ranking import RankingEngine


def create_candidate(symbol: str, score: str) -> CandidateScore:

    token = TokenMarket(
        address=symbol,
        symbol=symbol,
        name=f"{symbol} Token",
        updated_at=datetime.now(timezone.utc),
    )

    return CandidateScore(
        token=token,
        score=Decimal(score),
    )


candidates = [
    create_candidate("AAA", "72"),
    create_candidate("BBB", "95"),
    create_candidate("CCC", "81"),
    create_candidate("DDD", "99"),
    create_candidate("EEE", "65"),
]


ranking = RankingEngine.rank(
    candidates,
    limit=3,
)


print("===== TOP CANDIDATES =====")

for candidate in ranking:
    print(
        candidate.token.symbol,
        "->",
        candidate.score,
    )


if (
    ranking[0].token.symbol == "DDD"
    and ranking[1].token.symbol == "BBB"
    and ranking[2].token.symbol == "CCC"
):
    print("RANKING OK")
else:
    print("RANKING FAILED")