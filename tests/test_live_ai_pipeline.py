import asyncio
from decimal import Decimal

from app.ai.claude import ClaudeClient
from app.market.analysis.intelligence import MarketIntelligence
from app.market.providers.dexscreener import DexScreenerProvider
from app.market.scanner import TokenScanner


async def main():

    provider = DexScreenerProvider()
    claude = ClaudeClient()

    scanner = TokenScanner(
        min_liquidity_usd=Decimal("10000"),
        min_volume_5m_usd=Decimal("5000"),
        min_buys_5m=5,
    )

    intelligence = MarketIntelligence()

    try:

        # 1. Get live market data
        tokens = await provider.search_tokens("SOL")

        print()
        print("================================")
        print("       LIVE AI TRADING PIPELINE")
        print("================================")
        print()

        print(
            f"Market tokens : {len(tokens)}"
        )

        # 2. Scanner
        candidates = scanner.filter_candidates(
            tokens
        )

        print(
            f"Candidates    : {len(candidates)}"
        )

        if not candidates:
            print()
            print("No suitable candidates.")
            return

        # 3. Scoring + ranking + market analysis
        results = intelligence.analyze_tokens(
            candidates,
            limit=5,
        )

        print(
            f"Ranked tokens : {len(results)}"
        )

        print()
        print("TOP CANDIDATES")
        print("--------------------------------")

        for index, result in enumerate(
            results,
            start=1,
        ):

            token = result["token"]
            score = result["score"]
            analysis = result["analysis"]

            print(
                f"{index}. {token.symbol:<10} "
                f"Score={score} "
                f"Overall={analysis.overall_score}"
            )

        # 4. Select #1 candidate
        top = results[0]

        token = top["token"]
        analysis = top["analysis"]

        # 5. Prepare intelligence for Claude
        market_intelligence = {
            "token": {
                "address": token.address,
                "symbol": token.symbol,
                "name": token.name,
            },

            "system_score": str(
                top["score"]
            ),

            "market_analysis": {
                "momentum_score": str(
                    analysis.momentum_score
                ),
                "volume_score": str(
                    analysis.volume_score
                ),
                "pressure_score": str(
                    analysis.pressure_score
                ),
                "liquidity_score": str(
                    analysis.liquidity_score
                ),
                "overall_score": str(
                    analysis.overall_score
                ),
            },

            "market_data": {
                "price_usd": str(
                    token.price_usd
                ),
                "market_cap_usd": str(
                    token.market_cap_usd
                ),
                "liquidity_usd": str(
                    token.liquidity_usd
                ),
                "volume_5m_usd": str(
                    token.volume_5m_usd
                ),
                "volume_1h_usd": str(
                    token.volume_1h_usd
                ),
                "volume_24h_usd": str(
                    token.volume_24h_usd
                ),
                "price_change_5m": str(
                    token.price_change_5m
                ),
                "price_change_1h": str(
                    token.price_change_1h
                ),
                "price_change_24h": str(
                    token.price_change_24h
                ),
                "buys_5m": token.buys_5m,
                "sells_5m": token.sells_5m,
                "dex": token.dex,
            },
        }

        print()
        print("CLAUDE ANALYSIS")
        print("--------------------------------")

        # 6. Claude
        ai_result = await claude.analyze_market(
            market_intelligence
        )

        print(
            f"Token      : {token.symbol}"
        )

        print(
            f"Score      : {top['score']}"
        )

        print(
            f"Decision   : {ai_result.decision}"
        )

        print(
            f"Confidence : {ai_result.confidence}%"
        )

        print(
            f"Risk       : {ai_result.risk_level}"
        )

        print(
            f"Momentum   : {ai_result.momentum}"
        )

        print()
        print("Reasoning:")
        print(
            f"  {ai_result.reasoning}"
        )

        print()
        print("Invalidation:")

        for index, condition in enumerate(
            ai_result.invalidation,
            start=1,
        ):

            print(
                f"  {index}. {condition}"
            )

        print()
        print("================================")
        print("       LIVE AI PIPELINE OK")
        print("================================")

    finally:

        await provider.close()
        await claude.close()


if __name__ == "__main__":
    asyncio.run(main())