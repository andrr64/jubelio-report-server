# app/infrastructure/adapters/persistence/repository/tenant_repository_postgres.py
from app.application.protocols.database_port import DatabaseProvider
from app.application.protocols.tenant_repository_port import TenantRepositoryPort
from app.core.config import settings
from app.application.dto.db_config import DBConfig


class PostgresTenantRepository(TenantRepositoryPort):
    def __init__(self, db_provider: DatabaseProvider):
        self.db = db_provider

    async def get_db_config_by_company_id(self, company_id: int) -> DBConfig:
        query = """
                SELECT host, schema_name
                FROM tenant_company
                WHERE company_id = %(id)s
                """

        rows = await self.db.fetch_all(query, params={"id": company_id})

        if not rows:
            raise Exception(f"Database config not found for company_id: {company_id}")

        data = rows[0]
        host_val = data[0].decode('utf-8') if isinstance(data[0], bytes) else data[0]
        schema_val = data[1].decode('utf-8') if isinstance(data[1], bytes) else data[1]

        return DBConfig(
            host=host_val,
            port=settings.DB_PORT or 6432,
            username=settings.DB_USERNAME,
            password=settings.DB_PASSWORD,
            database="jb_tenant",
            schema=schema_val
        )
