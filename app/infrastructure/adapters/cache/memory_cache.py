import time
from typing import List, Dict, Any, Tuple

from app.application.protocols.database_port import DatabaseProvider  # Gunakan Protocol baru
from app.application.protocols.memory_cache_port import MemoryCachePort


class InMemoryMemoryCacheAdapter(MemoryCachePort):
    def __init__(self, db_fetcher: DatabaseProvider, ttl_seconds: int = 600):
        # db_fetcher di sini diasumsikan sudah di-init dengan System DB Config
        self.db_fetcher = db_fetcher
        self.ttl = ttl_seconds

        # Structure: { "key": (data_list, timestamp_float) }
        self._cache: Dict[str, Tuple[List[Dict[str, Any]], float]] = {}

    async def get_data(self, key: str, sql_query: str) -> List[Dict[str, Any]]:
        now = time.time()

        # 1. Cek Cache (Hit)
        if key in self._cache:
            data, timestamp = self._cache[key]
            if now - timestamp < self.ttl:
                return data

        # 2. Cache Miss / Expired -> Fetch DB
        # Perhatikan: Tidak perlu lagi passing config karena
        # PostgresqlProvider sudah menyimpannya di self.config
        rows = await self.db_fetcher.fetch_all_as_dict(
            sql=sql_query
        )

        result = rows or []

        # 3. Simpan ke Cache
        self._cache[key] = (result, now)

        return result
