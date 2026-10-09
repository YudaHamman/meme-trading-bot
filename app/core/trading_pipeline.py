import asyncio
from decimal import Decimal

from app.ai.claude import ClaudeClient
from app.market.analysis.intelligence import MarketIntelligence
from app.market.models import TokenMarket
from app.market.providers.dexscreener import DexScreenerProvider
from app.market.scanner import TokenScanner
from app.risk.engine import RiskEngine
from app.execution.paper_trader import PaperTrader
from app.execution.real_trader import RealSolanaTrader
from app.config.settings import settings


class TradingPipeline:

    def __init__(self):

        self.provider = DexScreenerProvider()

        self.scanner = TokenScanner(
            min_liquidity_usd=Decimal("10000"),
            min_volume_5m_usd=Decimal("5000"),
            min_buys_5m=5,
        )

        self.intelligence = MarketIntelligence()

        self.claude = ClaudeClient()

        self.risk_engine = RiskEngine()

        self.paper_trader = PaperTrader(
            take_profit_percent=Decimal("20"),
            stop_loss_percent=Decimal("10"),
        )

        self.real_trader = None

        if (
            settings.trading_mode.lower() == "real"
            or settings.real_trading_enabled
        ):
            self.real_trader = RealSolanaTrader()

    async def run(self):

        try:

            # 1. LIVE MARKET DATA

            tokens = await self.provider.search_tokens(
                "SOL"
            )

            print()
            print("================================")
            print("       TRADING PIPELINE")
            print("================================")
            print()

            print(
                f"Market tokens : {len(tokens)}"
            )

            # 2. SCANNER

            candidates = (
                self.scanner.filter_candidates(
                    tokens
                )
            )

            print(
                f"Candidates    : {len(candidates)}"
            )

            if not candidates:

                print()
                print("No candidates.")
                return

            # 3. INTELLIGENCE

            results = (
                self.intelligence.analyze_tokens(
                    candidates,
                    limit=5,
                )
            )

            if not results:

                print()
                print("No ranked tokens.")
                return

            # 4. TOP TOKEN

            top = results[0]

            token: TokenMarket = top["token"]

            analysis = top["analysis"]

            # 5. PREPARE CLAUDE DATA

            intelligence_data = {

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

            # 6. CLAUDE

            ai_result = (
                await self.claude.analyze_market(
                    intelligence_data
                )
            )

            print()
            print("TOP TOKEN")
            print("--------------------------------")

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

            # 7. RISK ENGINE

            risk_result = (
                self.risk_engine.evaluate(
                    token=token,
                    ai_analysis=ai_result,
                )
            )

            print()
            print("RISK ENGINE")
            print("--------------------------------")

            print(
                f"Approved      : "
                f"{risk_result.approved}"
            )

            print(
                f"Decision      : "
                f"{risk_result.decision}"
            )

            print(
                f"Position Size : "
                f"${risk_result.position_size_usd}"
            )

            for reason in risk_result.reasons:

                print(
                    f"  - {reason}"
                )

            # 8. TRADE EXECUTION

            if risk_result.approved:

                if self.real_trader is not None:

                    input_market = await self.provider.get_market(
                        settings.trade_input_mint
                    )

                    if not input_market:
                        raise RuntimeError(
                            "Input token market price was not found"
                        )

                    trade = await self.real_trader.open_position(
                        token_address=token.address,
                        symbol=token.symbol,
                        position_size_usd=(
                            risk_result.position_size_usd
                        ),
                        input_price_usd=(
                            input_market.price_usd
                        ),
                    )

                    print()
                    print("REAL TRADE")
                    print("--------------------------------")

                    print(
                        f"Action    : {trade.action}"
                    )

                    print(
                        f"Token     : {trade.symbol}"
                    )

                    print(
                        f"Signature : {trade.signature}"
                    )

                    print()
                    print(
                        "REAL POSITION OPENED"
                    )

                    output_amount = self._extract_output_amount(
                        trade.raw_result
                    )

                    if output_amount <= 0:
                        raise RuntimeError(
                            "Jupiter did not return a valid output token amount"
                        )

                    await self.monitor_real_position(
                        token=token,
                        token_amount=output_amount,
                        entry_price=token.price_usd,
                    )

                else:

                    trade = (
                        self.paper_trader.open_position(
                            token_address=token.address,
                            symbol=token.symbol,
                            entry_price=token.price_usd,
                            position_size_usd=(
                                risk_result
                                .position_size_usd
                            ),
                        )
                    )

                    print()
                    print("PAPER TRADE")
                    print("--------------------------------")

                    print(
                        f"Action : {trade.action}"
                    )

                    print(
                        f"Token  : {trade.symbol}"
                    )

                    print(
                        f"Price  : {trade.price}"
                    )

                    print()
                    print(
                        "PAPER POSITION OPENED"
                    )

            else:

                print()
                print(
                    "PAPER TRADE SKIPPED"
                )

            print()
            print("================================")
            print("       PIPELINE COMPLETE")
            print("================================")

        finally:

            await self.provider.close()
            await self.claude.close()
            if self.real_trader is not None:
                await self.real_trader.close()

    @staticmethod
    def _extract_output_amount(
        raw_result: dict | None,
    ) -> int:
        if raw_result is None:
            return 0

        value = (
            raw_result.get("totalOutputAmount")
            or raw_result.get("outputAmountResult")
            or "0"
        )

        try:
            return int(value)
        except (
            TypeError,
            ValueError,
        ):
            return 0

    async def monitor_real_position(
        self,
        *,
        token: TokenMarket,
        token_amount: int,
        entry_price: Decimal,
    ) -> None:
        take_profit_price = (
            entry_price
            * Decimal("1.20")
        )
        stop_loss_price = (
            entry_price
            * Decimal("0.90")
        )

        print()
        print("REAL POSITION MONITOR")
        print("--------------------------------")
        print(f"Token       : {token.symbol}")
        print(f"Entry       : {entry_price}")
        print(f"Take Profit : {take_profit_price}")
        print(f"Stop Loss   : {stop_loss_price}")

        while True:
            await asyncio.sleep(5)

            market = await self.provider.get_market(
                token.address
            )

            if not market:
                continue

            current_price = market.price_usd

            if current_price >= take_profit_price:
                result = await self.real_trader.close_position(
                    token_address=token.address,
                    symbol=token.symbol,
                    token_amount=token_amount,
                    action="TP",
                    price=current_price,
                )

                print()
                print("REAL TAKE PROFIT EXECUTED")
                print("--------------------------------")
                print(f"Signature : {result.signature}")
                return

            if current_price <= stop_loss_price:
                result = await self.real_trader.close_position(
                    token_address=token.address,
                    symbol=token.symbol,
                    token_amount=token_amount,
                    action="SL",
                    price=current_price,
                )

                print()
                print("REAL STOP LOSS EXECUTED")
                print("--------------------------------")
                print(f"Signature : {result.signature}")
                return
