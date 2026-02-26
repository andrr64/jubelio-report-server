# app/application/protocols/tenant_repository_port.py
from typing import Protocol

from app.application.dto.db_config import DBConfig


class TenantRepositoryPort(Protocol):
    async def get_db_config_by_company_id(self, company_id: int) -> DBConfig:
        pass
