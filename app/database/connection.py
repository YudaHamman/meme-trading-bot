import sqlite3
from pathlib import Path


DATABASE_DIR = Path("data")
DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATABASE_PATH = DATABASE_DIR / "trading_bot.db"


def get_connection():
    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection