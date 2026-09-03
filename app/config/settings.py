from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="meme-trading-bot")
    app_env: str = Field(default="development")
    app_version: str = Field(default="0.1.0")
    log_level: str = Field(default="INFO")

    # AI
    grok_api_key: str = Field(default="")

    # Solana
    solana_rpc_url: str = Field(default="")
    solana_ws_url: str = Field(default="")

    # Wallet
    trading_wallet_private_key: str = Field(default="")

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