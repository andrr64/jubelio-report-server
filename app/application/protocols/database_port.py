from typing import Protocol, List, Any, Union, Dict, Tuple, runtime_checkable


@runtime_checkable
class DatabaseProvider(Protocol):
    """
    Abstraksi database tanpa pooling.
    Setiap call bertanggung jawab atas lifecycle koneksi sendiri.
    """

    async def fetch_all(
            self, sql: str, params: Union[dict, tuple] = None
    ) -> List[Tuple]: ...

    async def fetch_all_as_dict(
            self, sql: str, params: Union[dict, tuple] = None
    ) -> List[Dict[str, Any]]: ...
