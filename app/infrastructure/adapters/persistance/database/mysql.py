from typing import Union, Tuple, List, Dict, Any

from app.application.protocols.database_port import DatabaseProvider


# another example: MySQL
class MySQLAdapter(DatabaseProvider):

    async def fetch_all(
            self, sql: str, params: Union[dict, tuple] = None
    ) -> List[Tuple]:
        pass

    async def fetch_all_as_dict(
            self, sql: str, params: Union[dict, tuple] = None
    ) -> List[Dict[str, Any]]:
        pass
