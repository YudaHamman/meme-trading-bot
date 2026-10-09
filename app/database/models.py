from app.database.connection import get_connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL UNIQUE,
            symbol TEXT,
            name TEXT,
            dex TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS market_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_address TEXT NOT NULL,
            price_usd TEXT,
            market_cap_usd TEXT,
            liquidity_usd TEXT,
            volume_5m_usd TEXT,
            volume_1h_usd TEXT,
            volume_24h_usd TEXT,
            price_change_5m TEXT,
            price_change_1h TEXT,
            price_change_24h TEXT,
            buys_5m INTEGER,
            sells_5m INTEGER,
            recorded_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ai_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_address TEXT NOT NULL,
            decision TEXT NOT NULL,
            confidence TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            momentum TEXT NOT NULL,
            reasoning TEXT,
            invalidation TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS risk_decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_address TEXT NOT NULL,
            approved INTEGER NOT NULL,
            decision TEXT NOT NULL,
            position_size_usd TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            reasons TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_address TEXT NOT NULL,
            symbol TEXT NOT NULL,
            entry_price TEXT NOT NULL,
            current_price TEXT NOT NULL,
            position_size_usd TEXT NOT NULL,
            quantity TEXT NOT NULL,
            take_profit_price TEXT NOT NULL,
            stop_loss_price TEXT NOT NULL,
            status TEXT NOT NULL,
            pnl_usd TEXT NOT NULL,
            pnl_percent TEXT NOT NULL,
            opened_at TEXT NOT NULL,
            closed_at TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_address TEXT NOT NULL,
            symbol TEXT NOT NULL,
            action TEXT NOT NULL,
            price TEXT NOT NULL,
            pnl_usd TEXT NOT NULL,
            pnl_percent TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()

    connection.close()