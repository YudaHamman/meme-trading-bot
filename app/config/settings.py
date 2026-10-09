from functools import lru_cache
from decimal import Decimal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="meme-trading-bot")
    app_env: str = Field(default="development")
    app_version: str = Field(default="0.1.0")
    log_level: str = Field(default="INFO")

    # AI
    claude_api_key: str = Field(default="")

    # Solana
    solana_rpc_url: str = Field(default="")
    solana_ws_url: str = Field(default="")

    # Wallet
    trading_wallet_private_key: str = Field(default="")

    # Real trading
    real_trading_enabled: bool = Field(default=False)
    trading_mode: str = Field(default="paper")
    jupiter_api_key: str = Field(default="")
    jupiter_base_url: str = Field(default="https://api.jup.ag/swap/v2")
    trade_input_mint: str = Field(
        default="So11111111111111111111111111111111111111112"
    )
    trade_input_decimals: int = Field(default=9)
    max_real_trade_usd: Decimal = Field(default=Decimal("5"))
    max_slippage_bps: int = Field(default=500)

    # Database
    database_url: str = Field(default="")

    # Telegram
    telegram_bot_token: str = Field(default="")
    telegram_chat_id: str = Field(default="")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
