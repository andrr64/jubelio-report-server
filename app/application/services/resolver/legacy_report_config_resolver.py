import re
from typing import Dict, Optional
from app.application.protocols.bucket_repository import BucketRepository
from app.core.logger import log


class LegacyReportConfigResolverService:
    """
    Analyzes SQL templates to identify and generate queries for global metadata injection.
    """
    _INJECTION_PATTERN = re.compile(
        r"jsonb_to_recordset\(@(\w+)(?:::\w+)?\)\s*as\s+x\((.*?)\)",
        re.IGNORECASE | re.DOTALL
    )

    # [FIX] 1. Inject BucketRepository ke sini
    def __init__(self, bucket_repo: BucketRepository):
        self.bucket_repo = bucket_repo

    # [FIX] 2. Ubah jadi async, dan terima tenant_id sebagai parameter
    async def resolve(self, tenant_id: str, report_name: str) -> Optional[str]:
        try:
            file_name = f"{report_name}.sql"

            log.info("=== RESOLVER DEBUG START ===")
            log.info(f"Tenant ID: {tenant_id}")
            log.info(f"Report Name: {report_name}")
            log.info(f"File Name (final): {file_name}")

            sql_text = await self.bucket_repo.get_report_sql(tenant_id, file_name)

            log.info("SQL berhasil diambil dari bucket")
            log.info("=== RESOLVER DEBUG END ===")

            return sql_text

        except Exception as e:
            log.error(f"Gagal resolve file SQL {report_name} untuk tenant {tenant_id} dari Bucket: {e}", exc_info=True)
            return None
    def scan_params_data_from_jb_system(self, sql_template: str) -> Optional[Dict[str, str]]:
        """
        Scans SQL for @table placeholders and generates the required SELECT statements.
        """
        matches = self._INJECTION_PATTERN.finditer(sql_template)
        required_queries = {}

        for match in matches:
            table_name = match.group(1)
            col_definitions = match.group(2)
            cols = [c.strip().split(' ')[0] for c in col_definitions.split(',')]
            col_string = ", ".join(cols)
            required_queries[table_name] = f"SELECT {col_string} FROM {table_name}"

        return required_queries if required_queries else None