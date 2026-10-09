from app.ai.models import AIAnalysisPayload


class AIPayloadBuilder:

    @staticmethod
    def build(
        result: dict,
    ) -> AIAnalysisPayload:

        market = result[
            "market"
        ]

        candidate = result[
            "candidate"
        ]

        intelligence = result[
            "intelligence"
        ]

        metadata = result[
            "metadata"
        ]

        return AIAnalysisPayload(

            mint=result[
                "mint"
            ],

            name=metadata.get(
                "name"
            ) or "",

            symbol=metadata.get(
                "symbol"
            ) or "",

            dex=market.dex,

            pair_address=(
                market.pair_address
            ),

            price_usd=(
                market.price_usd
            ),

            market_cap_usd=(
                market.market_cap_usd
            ),

            liquidity_usd=(
                market.liquidity_usd
            ),

            volume_5m_usd=(
                market.volume_5m_usd
            ),

            volume_1h_usd=(
                market.volume_1h_usd
            ),

            volume_24h_usd=(
                market.volume_24h_usd
            ),

            price_change_5m=(
                market.price_change_5m
            ),

            price_change_1h=(
                market.price_change_1h
            ),

            price_change_24h=(
                market.price_change_24h
            ),

            buys_5m=(
                market.buys_5m
            ),

            sells_5m=(
                market.sells_5m
            ),

            score=(
                candidate.score
            ),

            momentum=(
                intelligence[
                    "momentum"
                ]
            ),

            buy_pressure=(
                intelligence[
                    "buy_pressure"
                ]
            ),

            buy_pressure_status=(
                intelligence[
                    "buy_pressure_status"
                ]
            ),

            volume_status=(
                intelligence[
                    "volume_status"
                ]
            ),

            liquidity_status=(
                intelligence[
                    "liquidity_status"
                ]
            ),

            total_transactions_5m=(
                intelligence[
                    "total_transactions_5m"
                ]
            ),

            red_flags=(
                intelligence[
                    "red_flags"
                ]
            ),
        )