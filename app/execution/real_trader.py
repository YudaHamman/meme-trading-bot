import base64
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, ROUND_DOWN
from typing import Any

import httpx
from solders.keypair import Keypair
from solders.signature import Signature
from solders.transaction import VersionedTransaction

from app.config.settings import settings
from app.core.logger import logger
from app.execution.models import TradeResult


SOL_MINT = "So11111111111111111111111111111111111111112"


@dataclass(frozen=True)
class JupiterOrder:
    request_id: str
    transaction: str
    out_amount: str | None
    router: str | None
    mode: str | None
    raw: dict[str, Any]


class RealTradingConfigError(ValueError):
    pass


class JupiterSwapError(RuntimeError):
    pass


class RealSolanaTrader:

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        private_key: str | None = None,
        input_mint: str | None = None,
        input_decimals: int | None = None,
        max_slippage_bps: int | None = None,
        max_trade_usd: Decimal | None = None,
    ):
        self.api_key = api_key or settings.jupiter_api_key
        self.base_url = (
            base_url
            or settings.jupiter_base_url
        ).rstrip("/")
        self.input_mint = input_mint or settings.trade_input_mint
        self.input_decimals = (
            input_decimals
            if input_decimals is not None
            else settings.trade_input_decimals
        )
        self.max_slippage_bps = (
            max_slippage_bps
            if max_slippage_bps is not None
            else settings.max_slippage_bps
        )
        self.max_trade_usd = (
            max_trade_usd
            if max_trade_usd is not None
            else settings.max_real_trade_usd
        )

        key = private_key or settings.trading_wallet_private_key

        if not settings.real_trading_enabled:
            raise RealTradingConfigError(
                "REAL_TRADING_ENABLED must be true for live execution"
            )

        if not self.api_key:
            raise RealTradingConfigError(
                "JUPITER_API_KEY is required for live execution"
            )

        if not key:
            raise RealTradingConfigError(
                "TRADING_WALLET_PRIVATE_KEY is required for live execution"
            )

        self.keypair = Keypair.from_base58_string(
            key.strip()
        )
        self.wallet_address = str(
            self.keypair.pubkey()
        )
        self.client = httpx.AsyncClient(
            timeout=20
        )

    async def close(self) -> None:
        await self.client.aclose()

    def usd_to_input_amount(
        self,
        usd_amount: Decimal,
        input_price_usd: Decimal,
    ) -> int:
        if usd_amount <= 0:
            raise ValueError(
                "Trade size must be greater than zero"
            )

        if usd_amount > self.max_trade_usd:
            raise ValueError(
                "Trade size exceeds MAX_REAL_TRADE_USD"
            )

        if input_price_usd <= 0:
            raise ValueError(
                "Input token price must be greater than zero"
            )

        token_amount = (
            usd_amount
            / input_price_usd
        )
        smallest_unit = (
            token_amount
            * Decimal(10 ** self.input_decimals)
        ).quantize(
            Decimal("1"),
            rounding=ROUND_DOWN,
        )

        amount = int(smallest_unit)

        if amount <= 0:
            raise ValueError(
                "Calculated input amount is zero"
            )

        return amount

    async def open_position(
        self,
        *,
        token_address: str,
        symbol: str,
        position_size_usd: Decimal,
        input_price_usd: Decimal,
    ) -> TradeResult:
        amount = self.usd_to_input_amount(
            position_size_usd,
            input_price_usd,
        )

        result = await self.swap(
            input_mint=self.input_mint,
            output_mint=token_address,
            amount=amount,
        )

        if result.get("status") != "Success":
            raise JupiterSwapError(
                f"Jupiter swap failed: {result}"
            )

        signature = result.get("signature")

        logger.info(
            "REAL BUY %s | mint=%s | size_usd=%s | signature=%s",
            symbol,
            token_address,
            position_size_usd,
            signature,
        )

        return TradeResult(
            symbol=symbol,
            action="OPEN",
            price=Decimal("0"),
            timestamp=datetime.now(timezone.utc),
            signature=signature,
            raw_result=result,
        )

    async def close_position(
        self,
        *,
        token_address: str,
        symbol: str,
        token_amount: int,
        action: str,
        price: Decimal,
    ) -> TradeResult:
        if token_amount <= 0:
            raise ValueError(
                "Token amount must be greater than zero"
            )

        result = await self.swap(
            input_mint=token_address,
            output_mint=self.input_mint,
            amount=token_amount,
        )

        if result.get("status") != "Success":
            raise JupiterSwapError(
                f"Jupiter exit swap failed: {result}"
            )

        signature = result.get("signature")

        logger.info(
            "REAL %s %s | mint=%s | amount=%s | signature=%s",
            action,
            symbol,
            token_address,
            token_amount,
            signature,
        )

        return TradeResult(
            symbol=symbol,
            action=action,
            price=price,
            timestamp=datetime.now(timezone.utc),
            signature=signature,
            raw_result=result,
        )

    async def swap(
        self,
        *,
        input_mint: str,
        output_mint: str,
        amount: int,
    ) -> dict[str, Any]:
        order = await self.create_order(
            input_mint=input_mint,
            output_mint=output_mint,
            amount=amount,
        )

        signed_transaction = self.sign_transaction(
            order.transaction
        )

        return await self.execute_order(
            signed_transaction=signed_transaction,
            request_id=order.request_id,
            last_valid_block_height=(
                order.raw.get("lastValidBlockHeight")
            ),
        )

    async def create_order(
        self,
        *,
        input_mint: str | None = None,
        output_mint: str,
        amount: int,
    ) -> JupiterOrder:
        params: dict[str, str] = {
            "inputMint": input_mint or self.input_mint,
            "outputMint": output_mint,
            "amount": str(amount),
            "taker": self.wallet_address,
            "slippageBps": str(self.max_slippage_bps),
        }

        response = await self.client.get(
            f"{self.base_url}/order",
            params=params,
            headers=self._headers(),
        )

        if response.status_code >= 400:
            raise JupiterSwapError(
                f"Jupiter order failed: {response.status_code} "
                f"{response.text}"
            )

        data = response.json()
        transaction = data.get("transaction")

        if not transaction:
            raise JupiterSwapError(
                f"Jupiter order has no transaction: {data}"
            )

        return JupiterOrder(
            request_id=data["requestId"],
            transaction=transaction,
            out_amount=data.get("outAmount"),
            router=data.get("router"),
            mode=data.get("mode"),
            raw=data,
        )

    def sign_transaction(
        self,
        transaction_base64: str,
    ) -> str:
        transaction = VersionedTransaction.from_bytes(
            base64.b64decode(
                transaction_base64
            )
        )

        account_keys = list(
            transaction.message.account_keys
        )

        try:
            signer_index = account_keys.index(
                self.keypair.pubkey()
            )
        except ValueError as exc:
            raise JupiterSwapError(
                "Wallet is not a signer for Jupiter transaction"
            ) from exc

        signatures = list(
            transaction.signatures
        )

        required_signatures = (
            transaction
            .message
            .header
            .num_required_signatures
        )

        if signer_index >= required_signatures:
            raise JupiterSwapError(
                "Wallet account is present but is not a required signer"
            )

        while len(signatures) < required_signatures:
            signatures.append(
                Signature.default()
            )

        signatures[signer_index] = (
            self.keypair.sign_message(
                bytes(transaction.message)
            )
        )

        signed = VersionedTransaction.populate(
            transaction.message,
            signatures,
        )

        return base64.b64encode(
            bytes(signed)
        ).decode("ascii")

    async def execute_order(
        self,
        *,
        signed_transaction: str,
        request_id: str,
        last_valid_block_height: int | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "signedTransaction": signed_transaction,
            "requestId": request_id,
        }

        if last_valid_block_height is not None:
            body["lastValidBlockHeight"] = (
                last_valid_block_height
            )

        response = await self.client.post(
            f"{self.base_url}/execute",
            json=body,
            headers=self._headers(),
        )

        if response.status_code >= 400:
            raise JupiterSwapError(
                f"Jupiter execute failed: {response.status_code} "
                f"{response.text}"
            )

        return response.json()

    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }
