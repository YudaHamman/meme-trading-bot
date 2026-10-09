from datetime import datetime, timezone

from app.database.connection import get_connection
from app.market.models import TokenMarket


class TokenRepository:

    def save_token(
        self,
        token: TokenMarket,
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO tokens (
                address,
                symbol,
                name,
                dex,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)

            ON CONFLICT(address)
            DO UPDATE SET
                symbol = excluded.symbol,
                name = excluded.name,
                dex = excluded.dex
            """,
            (
                token.address,
                token.symbol,
                token.name,
                token.dex,
                datetime.now(
                    timezone.utc
                ).isoformat(),
            ),
        )

        connection.commit()

        connection.close()

    def get_token(
        self,
        address: str,
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM tokens
            WHERE address = ?
            """,
            (address,),
        )

        row = cursor.fetchone()

        connection.close()

        return row