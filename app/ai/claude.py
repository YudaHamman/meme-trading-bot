import json
from typing import Any

from anthropic import AsyncAnthropic

from app.ai.models import (
    AIAnalysis,
)

from app.ai.payload import (
    AIPayloadBuilder,
)

from app.config.settings import settings


class ClaudeAIEngine:

    def __init__(self):

        if not settings.claude_api_key:

            raise ValueError(
                "CLAUDE_API_KEY is not configured"
            )

        self.client = AsyncAnthropic(
            api_key=settings.claude_api_key
        )

        self.model = "claude-sonnet-4-6"

    @staticmethod
    def build_prompt(
        payload: Any,
    ) -> str:

        data = payload.model_dump(
            mode="json"
        )

        return f"""
You are a professional cryptocurrency
market analyst specializing in early-stage
Solana meme tokens.

Analyze the following token using ONLY
the supplied market data.

Your task is NOT to execute a trade.

IMPORTANT LANGUAGE RULE:

- Write "reasoning" in Indonesian.
- Write every "invalidation" item in Indonesian.
- Keep the decision values exactly:
  BUY, WATCH, or REJECT.
- Keep risk_level exactly:
  LOW, MEDIUM, or HIGH.
- Keep momentum exactly:
  BULLISH, NEUTRAL, or BEARISH.
- Do not translate these enum values.

Return exactly one JSON object with:

{{
  "decision": "BUY" | "WATCH" | "REJECT",
  "confidence": 0-100,
  "risk_level": "LOW" | "MEDIUM" | "HIGH",
  "momentum": "BULLISH" | "NEUTRAL" | "BEARISH",
  "reasoning": "penjelasan dalam bahasa Indonesia",
  "invalidation": [
    "kondisi pembatalan dalam bahasa Indonesia",
    "kondisi pembatalan dalam bahasa Indonesia"
  ]
}}

Decision guidelines:

BUY:
Gunakan hanya jika terdapat bukti yang cukup
bahwa momentum kuat, aktivitas transaksi sehat,
likuiditas memadai, dan tidak terdapat red flag
utama.

WATCH:
Gunakan jika momentum atau aktivitas terlihat
menarik tetapi bukti yang tersedia belum cukup
untuk BUY.

REJECT:
Gunakan jika kondisi pasar atau sinyal risiko
membuat token tidak layak untuk dipertimbangkan.

Important:

- Jangan mengarang data.
- Jika liquidity = 0, anggap sebagai ketidakpastian besar.
- Buy pressure tinggi saja TIDAK cukup untuk BUY.
- Jangan menganggap token aman.
- Jangan menjamin keuntungan.
- Jangan memberikan instruksi eksekusi trading.
- Reasoning harus ringkas tetapi jelas.
- Return valid JSON only.

TOKEN DATA:

{json.dumps(
    data,
    indent=2,
    default=str
)}
"""

    async def analyze(
        self,
        result: dict,
    ) -> AIAnalysis:

        payload = (
            AIPayloadBuilder.build(
                result
            )
        )

        prompt = (
            self.build_prompt(
                payload
            )
        )

        response = await (
            self.client.messages.create(
                model=self.model,
                max_tokens=700,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
        )

        text = ""

        for block in response.content:

            if hasattr(
                block,
                "text",
            ):

                text += block.text

        text = text.strip()

        # =====================================
        # REMOVE MARKDOWN JSON FENCE
        # =====================================

        if text.startswith(
            "```json"
        ):

            text = text[7:]

            if text.endswith(
                "```"
            ):

                text = text[:-3]

            text = text.strip()

        elif text.startswith(
            "```"
        ):

            text = text[3:]

            if text.endswith(
                "```"
            ):

                text = text[:-3]

            text = text.strip()

        # =====================================
        # PARSE JSON
        # =====================================

        try:

            data = json.loads(
                text
            )

        except json.JSONDecodeError as exc:

            raise ValueError(
                "Claude returned invalid JSON: "
                f"{text}"
            ) from exc

        # =====================================
        # VALIDATE RESPONSE
        # =====================================

        return AIAnalysis.model_validate(
            data
        )

    async def close(self) -> None:
        close = getattr(
            self.client,
            "close",
            None,
        )

        if close is not None:
            await close()


class ClaudeClient:

    def __init__(self):

        if not settings.claude_api_key:

            raise ValueError(
                "CLAUDE_API_KEY is not configured"
            )

        self.client = AsyncAnthropic(
            api_key=settings.claude_api_key
        )

        self.model = "claude-sonnet-4-6"

    async def ask(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 700,
    ) -> str:

        response = await (
            self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
            )
        )

        return self._extract_text(response)

    async def analyze_token(
        self,
        market_data: dict,
    ) -> AIAnalysis:

        return await self.analyze_market(
            {
                "token": {
                    "address": market_data.get(
                        "address",
                        "",
                    ),
                    "symbol": market_data.get(
                        "symbol",
                        "",
                    ),
                    "name": market_data.get(
                        "name",
                        "",
                    ),
                },
                "market_data": market_data,
            }
        )

    async def analyze_market(
        self,
        market_intelligence: dict,
    ) -> AIAnalysis:

        prompt = self._build_market_prompt(
            market_intelligence
        )

        text = await self.ask(
            system_prompt=(
                "You are a professional cryptocurrency market "
                "analyst specializing in early-stage Solana meme tokens."
            ),
            user_prompt=prompt,
        )

        return self._parse_analysis(text)

    async def close(self) -> None:

        close = getattr(
            self.client,
            "close",
            None,
        )

        if close is not None:
            await close()

    @staticmethod
    def _extract_text(response: Any) -> str:

        text = ""

        for block in response.content:

            if hasattr(
                block,
                "text",
            ):

                text += block.text

        return text.strip()

    @staticmethod
    def _parse_analysis(text: str) -> AIAnalysis:

        text = text.strip()

        if text.startswith(
            "```json"
        ):

            text = text[7:]

            if text.endswith(
                "```"
            ):

                text = text[:-3]

            text = text.strip()

        elif text.startswith(
            "```"
        ):

            text = text[3:]

            if text.endswith(
                "```"
            ):

                text = text[:-3]

            text = text.strip()

        try:

            data = json.loads(
                text
            )

        except json.JSONDecodeError as exc:

            raise ValueError(
                "Claude returned invalid JSON: "
                f"{text}"
            ) from exc

        return AIAnalysis.model_validate(
            data
        )

    @staticmethod
    def _build_market_prompt(
        market_intelligence: dict,
    ) -> str:

        return f"""
Analyze the following token using ONLY
the supplied market data.

Your task is NOT to execute a trade.

IMPORTANT LANGUAGE RULE:

- Write "reasoning" in Indonesian.
- Write every "invalidation" item in Indonesian.
- Keep the decision values exactly:
  BUY, WATCH, or REJECT.
- Keep risk_level exactly:
  LOW, MEDIUM, or HIGH.
- Keep momentum exactly:
  BULLISH, NEUTRAL, or BEARISH.
- Do not translate these enum values.

Return exactly one JSON object with:

{{
  "decision": "BUY" | "WATCH" | "REJECT",
  "confidence": 0-100,
  "risk_level": "LOW" | "MEDIUM" | "HIGH",
  "momentum": "BULLISH" | "NEUTRAL" | "BEARISH",
  "reasoning": "penjelasan dalam bahasa Indonesia",
  "invalidation": [
    "kondisi pembatalan dalam bahasa Indonesia",
    "kondisi pembatalan dalam bahasa Indonesia"
  ]
}}

Decision guidelines:

BUY:
Gunakan hanya jika terdapat bukti yang cukup
bahwa momentum kuat, aktivitas transaksi sehat,
likuiditas memadai, dan tidak terdapat red flag
utama.

WATCH:
Gunakan jika momentum atau aktivitas terlihat
menarik tetapi bukti yang tersedia belum cukup
untuk BUY.

REJECT:
Gunakan jika kondisi pasar atau sinyal risiko
membuat token tidak layak untuk dipertimbangkan.

Important:

- Jangan mengarang data.
- Jika liquidity = 0, anggap sebagai ketidakpastian besar.
- Buy pressure tinggi saja TIDAK cukup untuk BUY.
- Jangan menganggap token aman.
- Jangan menjamin keuntungan.
- Jangan memberikan instruksi eksekusi trading.
- Reasoning harus ringkas tetapi jelas.
- Return valid JSON only.

TOKEN DATA:

{json.dumps(
    market_intelligence,
    indent=2,
    default=str
)}
"""
