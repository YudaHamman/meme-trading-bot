import asyncio
from typing import Any

from app.ai.claude import ClaudeAIEngine

from app.market.providers.solana_ws import (
    SolanaWebSocket,
)

from app.market.providers.pump_create_detector import (
    PumpCreateDetector,
)

from app.market.providers.pump_discovery import (
    PumpTokenDiscovery,
)

from app.market.providers.token_metadata import (
    TokenMetadataExtractor,
)

from app.market.providers.dexscreener import (
    DexScreenerProvider,
)

from app.market.scoring.engine import (
    ScoringEngine,
)

from app.market.scoring.filter import (
    CandidateFilter,
)

from app.market.analysis.intelligence import (
    MarketIntelligence,
)

from app.risk.engine import (
    RiskEngine,
)

from app.execution.paper_trader import (
    PaperTrader,
)

from app.execution.position_monitor import (
    PositionMonitor,
)

from app.execution.paper_position_service import (
    PaperPositionService,
)


PUMP_PROGRAM_ID = (
    "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
)


class LiveDiscoveryPipeline:

    def __init__(self):

        self.ws = SolanaWebSocket()

        self.discovery = PumpTokenDiscovery()

        self.metadata = TokenMetadataExtractor()

        self.market = DexScreenerProvider()

        self.scoring = ScoringEngine()

        self.filter = CandidateFilter()

        self.intelligence = MarketIntelligence()

        self.claude = ClaudeAIEngine()

        self.risk = RiskEngine()

        self.paper_trader = PaperTrader()

        self.position_monitor = PositionMonitor(
            self.paper_trader
        )

        self.paper_position_service = (
            PaperPositionService(
                paper_trader=self.paper_trader,
                position_monitor=self.position_monitor,
                market_provider=self.market,
                poll_interval_seconds=5.0,
            )
        )

        self.monitor_tasks: set[asyncio.Task] = set()

        # =====================================
        # LIVE DISCOVERY STATISTICS
        # =====================================

        self.stats = {
            "create_detected": 0,
            "transaction_found": 0,
            "mint_found": 0,
            "metadata_found": 0,
            "market_found": 0,
            "candidate_passed": 0,
            "candidate_rejected": 0,
            "claude_analyzed": 0,
            "risk_approved": 0,
            "risk_rejected": 0,
            "paper_trades": 0,
        }

        self.filter_rejections: dict[str, int] = {}

    # =====================================
    # STATISTICS
    # =====================================

    def print_stats(self):

        print()
        print(
            "================================"
        )

        print(
            "       LIVE DISCOVERY STATS"
        )

        print(
            "================================"
        )

        print(
            "Create detected       :",
            self.stats["create_detected"]
        )

        print(
            "Transaction found     :",
            self.stats["transaction_found"]
        )

        print(
            "Mint found             :",
            self.stats["mint_found"]
        )

        print(
            "Metadata found         :",
            self.stats["metadata_found"]
        )

        print(
            "Market found           :",
            self.stats["market_found"]
        )

        print(
            "Candidate passed       :",
            self.stats["candidate_passed"]
        )

        print(
            "Candidate rejected     :",
            self.stats["candidate_rejected"]
        )

        print(
            "Claude analyzed        :",
            self.stats["claude_analyzed"]
        )

        print(
            "Risk approved          :",
            self.stats["risk_approved"]
        )

        print(
            "Risk rejected          :",
            self.stats["risk_rejected"]
        )

        print(
            "Paper trades           :",
            self.stats["paper_trades"]
        )

        print(
            "================================"
        )

        if self.filter_rejections:

            print()
            print(
                "FILTER REJECTION REASONS"
            )

            print(
                "================================"
            )

            sorted_rejections = sorted(
                self.filter_rejections.items(),
                key=lambda item: item[1],
                reverse=True,
            )

            for reason, count in sorted_rejections:

                print(
                    f"{reason:<32}: {count}"
                )

            print(
                "================================"
            )

    # =====================================
    # RETRY TRANSACTION
    # =====================================

    async def get_transaction_with_retry(
        self,
        signature: str,
        max_attempts: int = 10,
        delay_seconds: float = 1.0,
    ):

        for attempt in range(
            1,
            max_attempts + 1,
        ):

            print(
                f"TRANSACTION ATTEMPT "
                f"{attempt}/{max_attempts}"
            )

            try:

                transaction = (
                    await self.discovery
                    .get_transaction(
                        signature
                    )
                )

                if transaction:

                    print(
                        "TRANSACTION FOUND"
                    )

                    self.stats[
                        "transaction_found"
                    ] += 1

                    return transaction

            except Exception as exc:

                print(
                    "TRANSACTION ERROR:",
                    exc
                )

            if attempt < max_attempts:

                await asyncio.sleep(
                    delay_seconds
                )

        print(
            "TRANSACTION NOT FOUND "
            "AFTER RETRIES"
        )

        return None

    # =====================================
    # RETRY MARKET
    # =====================================

    async def get_market_with_retry(
        self,
        mint: str,
        max_attempts: int = 10,
        delay_seconds: float = 2.0,
    ):

        for attempt in range(
            1,
            max_attempts + 1,
        ):

            print(
                f"MARKET ATTEMPT "
                f"{attempt}/{max_attempts}"
            )

            try:

                market = (
                    await self.market
                    .get_market(
                        mint
                    )
                )

                if market:

                    print(
                        "MARKET FOUND"
                    )

                    self.stats[
                        "market_found"
                    ] += 1

                    return market

            except Exception as exc:

                print(
                    "MARKET ERROR:",
                    exc
                )

            if attempt < max_attempts:

                print(
                    "PAIR NOT INDEXED YET..."
                )

                await asyncio.sleep(
                    delay_seconds
                )

        print(
            "MARKET NOT FOUND "
            "AFTER RETRIES"
        )

        return None

    # =====================================
    # POSITION MONITOR
    # =====================================

    def start_position_monitor(
        self,
        mint: str,
    ):

        if mint not in self.paper_trader.positions:

            print(
                "NO POSITION TO MONITOR:",
                mint
            )

            return None

        position = (
            self.paper_trader.positions[mint]
        )

        if position.status != "OPEN":

            print(
                "POSITION IS NOT OPEN:",
                mint
            )

            return None

        print()
        print(
            "STARTING POSITION MONITOR"
        )

        print(
            "MINT:",
            mint
        )

        task = asyncio.create_task(
            self.paper_position_service
            .monitor_position(
                token_address=mint
            )
        )

        self.monitor_tasks.add(
            task
        )

        task.add_done_callback(
            self.monitor_tasks.discard
        )

        print(
            "MONITOR TASK STARTED"
        )

        print(
            "ACTIVE MONITORS:",
            len(self.monitor_tasks)
        )

        return task

    async def stop_position_monitors(self):

        if not self.monitor_tasks:

            return

        print()
        print(
            "STOPPING POSITION MONITORS..."
        )

        tasks = list(
            self.monitor_tasks
        )

        for task in tasks:

            if not task.done():

                task.cancel()

        await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

        self.monitor_tasks.clear()

        print(
            "POSITION MONITORS STOPPED"
        )

    # =====================================
    # PROCESS SIGNATURE
    # =====================================

    async def process_signature(
        self,
        signature: str,
    ) -> dict[str, Any] | None:

        print()
        print(
            "PROCESSING SIGNATURE:"
        )

        print(signature)

        # =====================================
        # STEP 1 - TRANSACTION
        # =====================================

        print()
        print(
            "STEP 1: GET TRANSACTION"
        )

        transaction = (
            await self.get_transaction_with_retry(
                signature,
                max_attempts=10,
                delay_seconds=1.0,
            )
        )

        if not transaction:

            print(
                "FAILED: TRANSACTION NOT FOUND"
            )

            return None

        print(
            "OK: TRANSACTION FOUND"
        )

        # =====================================
        # STEP 2 - MINT
        # =====================================

        print()
        print(
            "STEP 2: FIND MINT"
        )

        try:

            mint = (
                self.discovery
                .find_mint(
                    transaction
                )
            )

        except Exception as exc:

            print(
                "FAILED: FIND MINT"
            )

            print(
                "ERROR:",
                exc
            )

            return None

        if not mint:

            print(
                "FAILED: MINT NOT FOUND"
            )

            return None

        self.stats[
            "mint_found"
        ] += 1

        print(
            "OK: MINT FOUND"
        )

        print(
            "MINT:",
            mint
        )

        # =====================================
        # STEP 3 - METADATA
        # =====================================

        print()
        print(
            "STEP 3: GET METADATA"
        )

        try:

            metadata = (
                await self.metadata
                .get_metadata_with_retry(
                    mint,
                    max_attempts=10,
                    delay_seconds=1.0,
                )
            )

        except Exception as exc:

            print(
                "FAILED: GET METADATA"
            )

            print(
                "ERROR:",
                exc
            )

            return None

        if not metadata:

            print(
                "FAILED: METADATA NOT FOUND"
            )

            return None

        self.stats[
            "metadata_found"
        ] += 1

        print(
            "OK: METADATA FOUND"
        )

        print(
            "NAME:",
            metadata.get("name")
        )

        print(
            "SYMBOL:",
            metadata.get("symbol")
        )

        # =====================================
        # STEP 4 - MARKET
        # =====================================

        print()
        print(
            "STEP 4: GET MARKET"
        )

        market = (
            await self.get_market_with_retry(
                mint,
                max_attempts=10,
                delay_seconds=2.0,
            )
        )

        if not market:

            print(
                "FAILED: MARKET NOT FOUND"
            )

            return None

        print(
            "OK: MARKET FOUND"
        )

        print(
            "DEX:",
            market.dex
        )

        print(
            "PAIR:",
            market.pair_address
        )

        print(
            "PRICE:",
            market.price_usd
        )

        print(
            "LIQUIDITY:",
            market.liquidity_usd
        )

        print(
            "VOLUME 5M:",
            market.volume_5m_usd
        )

        print(
            "BUYS 5M:",
            market.buys_5m
        )

        print(
            "SELLS 5M:",
            market.sells_5m
        )

        # =====================================
        # STEP 5 - SCORING
        # =====================================

        print()
        print(
            "STEP 5: CALCULATE SCORE"
        )

        try:

            candidate = (
                self.scoring
                .calculate(
                    market
                )
            )

        except Exception as exc:

            print(
                "FAILED: CALCULATE SCORE"
            )

            print(
                "ERROR:",
                exc
            )

            return None

        print(
            "OK: SCORE CALCULATED"
        )

        print(
            "SCORE:",
            candidate.score
        )

        # =====================================
        # STEP 6 - CANDIDATE FILTER
        # =====================================

        print()
        print(
            "STEP 6: CANDIDATE FILTER"
        )

        try:

            passed, reasons = (
                self.filter.check(
                    market,
                    score=candidate.score,
                )
            )

        except Exception as exc:

            print(
                "FAILED: CANDIDATE FILTER"
            )

            print(
                "ERROR:",
                exc
            )

            return None

        # =====================================
        # FILTER EXPLANATION
        # =====================================

        try:

            filter_explanation = (
                self.filter.explain(
                    market,
                    score=candidate.score,
                )
            )

            print()
            print(
                "CANDIDATE FILTER ANALYSIS"
            )

            print(
                "--------------------------------"
            )

            volume_data = (
                filter_explanation[
                    "volume_5m"
                ]
            )

            print(
                "Volume 5M:",
                volume_data["value"],
                "/",
                volume_data["minimum"],
                "PASS"
                if volume_data["passed"]
                else "FAIL",
            )

            transaction_data = (
                filter_explanation[
                    "transactions_5m"
                ]
            )

            print(
                "Transactions 5M:",
                transaction_data["value"],
                "/",
                transaction_data["minimum"],
                "PASS"
                if transaction_data["passed"]
                else "FAIL",
            )

            buy_ratio_data = (
                filter_explanation[
                    "buy_ratio"
                ]
            )

            print(
                "Buy Ratio:",
                buy_ratio_data["value"] * 100,
                "%",
                "PASS"
                if buy_ratio_data["passed"]
                else "FAIL",
            )

            liquidity_data = (
                filter_explanation[
                    "liquidity_usd"
                ]
            )

            print(
                "Liquidity:",
                liquidity_data["value"],
                "/",
                liquidity_data["minimum"],
                "PASS"
                if liquidity_data["passed"]
                else "FAIL",
            )

            score_data = (
                filter_explanation[
                    "score"
                ]
            )

            print(
                "Score:",
                score_data["value"],
                "/",
                score_data["minimum"],
                "PASS"
                if score_data["passed"]
                else "FAIL",
            )

            price_data = (
                filter_explanation[
                    "price_change_5m"
                ]
            )

            print(
                "Price Change 5M:",
                price_data["value"],
                "%",
                "PASS"
                if price_data["passed"]
                else "FAIL",
            )

            print(
                "--------------------------------"
            )

        except Exception as exc:

            print(
                "FILTER EXPLANATION ERROR:",
                exc
            )

        # =====================================
        # FILTER REJECTED
        # =====================================

        if not passed:

            self.stats[
                "candidate_rejected"
            ] += 1

            for reason in reasons:

                self.filter_rejections[
                    reason
                ] = (
                    self.filter_rejections
                    .get(reason, 0)
                    + 1
                )

            print()
            print(
                "❌ CANDIDATE REJECTED"
            )

            print(
                "REASONS:"
            )

            for reason in reasons:

                print(
                    "-",
                    reason
                )

            return None

        self.stats[
            "candidate_passed"
        ] += 1

        print()
        print(
            "✅ CANDIDATE PASSED"
        )

        # =====================================
        # STEP 7 - MARKET INTELLIGENCE
        # =====================================

        print()
        print(
            "STEP 7: MARKET INTELLIGENCE"
        )

        try:

            intelligence = (
                self.intelligence
                .analyze(
                    market
                )
            )

        except Exception as exc:

            print(
                "FAILED: MARKET INTELLIGENCE"
            )

            print(
                "ERROR:",
                exc
            )

            return None

        print(
            "OK: MARKET INTELLIGENCE"
        )

        print(
            "MOMENTUM:",
            intelligence["momentum"]
        )

        print(
            "BUY PRESSURE:",
            intelligence["buy_pressure"],
            "%"
        )

        print(
            "BUY PRESSURE STATUS:",
            intelligence[
                "buy_pressure_status"
            ]
        )

        print(
            "VOLUME STATUS:",
            intelligence[
                "volume_status"
            ]
        )

        print(
            "LIQUIDITY STATUS:",
            intelligence[
                "liquidity_status"
            ]
        )

        print(
            "TRANSACTIONS 5M:",
            intelligence[
                "total_transactions_5m"
            ]
        )

        print(
            "RED FLAGS:",
            intelligence[
                "red_flags"
            ]
        )

        # =====================================
        # STEP 8 - CLAUDE AI
        # =====================================

        print()
        print(
            "STEP 8: CLAUDE AI ANALYSIS"
        )

        ai_result = {

            "mint": mint,

            "metadata": metadata,

            "market": market,

            "candidate": candidate,

            "filter_passed": passed,

            "filter_reasons": reasons,

            "intelligence": intelligence,
        }

        try:

            analysis = (
                await self.claude
                .analyze(
                    ai_result
                )
            )

        except Exception as exc:

            print(
                "FAILED: CLAUDE AI"
            )

            print(
                "ERROR:",
                exc
            )

            return None

        self.stats[
            "claude_analyzed"
        ] += 1

        print()
        print(
            "================================"
        )

        print(
            "🤖 CLAUDE ANALYSIS"
        )

        print(
            "================================"
        )

        print(
            "DECISION:",
            analysis.decision
        )

        print(
            "CONFIDENCE:",
            analysis.confidence
        )

        print(
            "RISK:",
            analysis.risk_level
        )

        print(
            "MOMENTUM:",
            analysis.momentum
        )

        print()

        print(
            "REASONING:"
        )

        print(
            analysis.reasoning
        )

        print()

        print(
            "INVALIDATION:"
        )

        for item in analysis.invalidation:

            print(
                "-",
                item
            )

        print(
            "================================"
        )

        # =====================================
        # STEP 9 - RISK ENGINE
        # =====================================

        print()
        print(
            "STEP 9: RISK ENGINE"
        )

        try:

            risk_decision = (
                self.risk
                .evaluate(
                    decision=analysis.decision,
                    confidence=analysis.confidence,
                    risk_level=analysis.risk_level,
                    liquidity_usd=market.liquidity_usd,
                )
            )

        except Exception as exc:

            print(
                "FAILED: RISK ENGINE"
            )

            print(
                "ERROR:",
                exc
            )

            return None

        print()
        print(
            "================================"
        )

        print(
            "🛡️ RISK ENGINE"
        )

        print(
            "================================"
        )

        print(
            "APPROVED:",
            risk_decision.approved
        )

        print(
            "DECISION:",
            risk_decision.decision
        )

        print(
            "POSITION SIZE:",
            risk_decision.position_size_usd
        )

        print(
            "RISK LEVEL:",
            risk_decision.risk_level
        )

        print()

        if risk_decision.reasons:

            print(
                "RISK REASONS:"
            )

            for reason in risk_decision.reasons:

                print(
                    "-",
                    reason
                )

        else:

            print(
                "RISK REASONS: NONE"
            )

        print(
            "================================"
        )

        # =====================================
        # RISK REJECTED
        # =====================================

        if not risk_decision.approved:

            self.stats[
                "risk_rejected"
            ] += 1

            print()
            print(
                "❌ RISK ENGINE REJECTED"
            )

            print(
                "NO PAPER TRADE WILL BE OPENED"
            )

            return {
                "signature": signature,
                "mint": mint,
                "metadata": metadata,
                "market": market,
                "candidate": candidate,
                "filter_passed": passed,
                "filter_reasons": reasons,
                "intelligence": intelligence,
                "ai_analysis": analysis,
                "risk_decision": risk_decision,
                "paper_trade": None,
                "position": None,
            }

        self.stats[
            "risk_approved"
        ] += 1

        # =====================================
        # STEP 10 - PAPER TRADING
        # =====================================

        print()
        print(
            "STEP 10: PAPER TRADING"
        )

        symbol = (
            metadata.get("symbol")
            or market.symbol
            or "UNKNOWN"
        )

        try:

            paper_trade = (
                self.paper_trader
                .open_position(
                    token_address=mint,
                    symbol=symbol,
                    entry_price=market.price_usd,
                    position_size_usd=(
                        risk_decision
                        .position_size_usd
                    ),
                )
            )

        except Exception as exc:

            print(
                "FAILED: PAPER TRADING"
            )

            print(
                "ERROR:",
                exc
            )

            return None

        self.stats[
            "paper_trades"
        ] += 1

        position = (
            self.paper_trader
            .positions[mint]
        )

        print()
        print(
            "================================"
        )

        print(
            "📄 PAPER TRADE"
        )

        print(
            "================================"
        )

        print(
            "ACTION:",
            paper_trade.action
        )

        print(
            "SYMBOL:",
            symbol
        )

        print(
            "ENTRY PRICE:",
            position.entry_price
        )

        print(
            "POSITION SIZE:",
            position.position_size_usd
        )

        print(
            "QUANTITY:",
            position.quantity
        )

        print(
            "TAKE PROFIT:",
            position.take_profit_price
        )

        print(
            "STOP LOSS:",
            position.stop_loss_price
        )

        print(
            "STATUS:",
            position.status
        )

        print(
            "================================"
        )

        print()
        print(
            "✅ PAPER POSITION OPENED"
        )

        # =====================================
        # STEP 11 - POSITION MONITOR
        # =====================================

        print()
        print(
            "STEP 11: POSITION MONITOR"
        )

        self.start_position_monitor(
            mint
        )

        # =====================================
        # FINAL RESULT
        # =====================================

        return {
            "signature": signature,
            "mint": mint,
            "metadata": metadata,
            "market": market,
            "candidate": candidate,
            "filter_passed": passed,
            "filter_reasons": reasons,
            "intelligence": intelligence,
            "ai_analysis": analysis,
            "risk_decision": risk_decision,
            "paper_trade": paper_trade,
            "position": position,
        }

    # =====================================
    # LIVE LISTENER
    # =====================================

    async def listen(
        self,
        duration: int = 120,
    ):

        await self.ws.connect()

        try:

            response = (
                await self.ws.logs_subscribe(
                    PUMP_PROGRAM_ID
                )
            )

            print()
            print(
                "SUBSCRIBED:",
                response
            )

            print()
            print(
                "LISTENING FOR REAL CREATE..."
            )

            print(
                "Press CTRL+C to stop"
            )

            print()

            async with asyncio.timeout(
                duration
            ):

                async for event in (
                    self.ws.listen()
                ):

                    params = event.get(
                        "params",
                        {}
                    )

                    result = params.get(
                        "result",
                        {}
                    )

                    value = result.get(
                        "value",
                        {}
                    )

                    if value.get(
                        "err"
                    ) is not None:

                        continue

                    logs = value.get(
                        "logs",
                        []
                    )

                    if not logs:

                        continue

                    if not (
                        PumpCreateDetector
                        .is_create_event(
                            event
                        )
                    ):

                        continue

                    signature = value.get(
                        "signature"
                    )

                    if not signature:

                        continue

                    self.stats[
                        "create_detected"
                    ] += 1

                    instruction = (
                        PumpCreateDetector
                        .get_create_instruction(
                            event
                        )
                    )

                    print()
                    print(
                        "================================"
                    )

                    print(
                        "🔥 REAL CREATE DETECTED"
                    )

                    print(
                        "SIGNATURE:",
                        signature
                    )

                    print(
                        "INSTRUCTION:",
                        instruction
                    )

                    print(
                        "TOTAL CREATES:",
                        self.stats[
                            "create_detected"
                        ]
                    )

                    print(
                        "================================"
                    )

                    processed = (
                        await self
                        .process_signature(
                            signature
                        )
                    )

                    if processed:

                        yield processed

                        print()
                        print(
                            "================================"
                        )

                        print(
                            "LISTENER STILL RUNNING"
                        )

                        print(
                            "ACTIVE MONITORS:",
                            len(self.monitor_tasks)
                        )

                        print(
                            "WAITING FOR NEXT CREATE..."
                        )

                        print(
                            "================================"
                        )

                        continue

                    print()
                    print(
                        "CREATE PROCESSING FAILED"
                    )

                    print(
                        "WAITING FOR NEXT CREATE..."
                    )

        except TimeoutError:

            print()
            print(
                "LIVE DISCOVERY TIMEOUT"
            )

        except asyncio.CancelledError:

            print()
            print(
                "LIVE DISCOVERY CANCELLED"
            )

            raise

        finally:

            self.print_stats()

            await self.stop_position_monitors()

            await self.ws.close()

            print()
            print(
                "LIVE DISCOVERY STOPPED"
            )