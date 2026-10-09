from app.market.scoring.engine import CandidateScore


class RankingEngine:

    @staticmethod
    def rank(
        candidates: list[CandidateScore],
        limit: int = 10,
    ) -> list[CandidateScore]:

        ranked = sorted(
            candidates,
            key=lambda candidate: candidate.score,
            reverse=True,
        )

        return ranked[:limit]