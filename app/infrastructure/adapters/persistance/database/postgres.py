# app.infrastructure.persistance.database.postgres
from typing import Union, List, Tuple, Dict, Any

import psycopg
from psycopg.rows import dict_row

from app.application.protocols.database_port import DatabaseProvider
from app.application.dto.db_config import DBConfig


class PostgresAdapter(DatabaseProvider):
    def __init__(self, config: DBConfig):
        self.config = config
        self._dsn = (
            f"postgresql://{config.username}:{config.password}@"
            f"{config.host}:{config.port}/{config.database}"
        )

    async def _get_connection(self, autocommit: bool = True) -> psycopg.AsyncConnection:
        """Helper untuk membuat koneksi baru (Handshake ulang)."""
        return await psycopg.AsyncConnection.connect(
            conninfo=self._dsn,
            autocommit=autocommit,
            # [FIX] Pastikan driver selalu decode ke UTF-8 string
            client_encoding="utf8",
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5
        )

    async def fetch_all(self, sql: str, params: Union[dict, tuple] = None) -> List[Tuple]:
        async with await self._get_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, params)
                return await cur.fetchall()

    async def fetch_all_as_dict(self, sql: str, params: Union[dict, tuple] = None) -> List[Dict[str, Any]]:
        async with await self._get_connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(sql, params)
                return await cur.fetchall()
