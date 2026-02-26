from typing import Protocol, List, Dict, Any


class MemoryCachePort(Protocol):
    """
    Kontrak untuk mengambil data master (System DB).
    Implementasinya wajib menangani Caching.
    """

    async def get_data(self, key: str, sql_query: str) -> List[Dict[str, Any]]:
        ...
