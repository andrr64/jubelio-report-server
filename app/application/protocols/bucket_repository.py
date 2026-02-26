from typing import Protocol


class BucketRepository(Protocol):

    async def get_report_sql(self, tenant_id: str, file_name: str) -> str:
        """
        Ambil file .sql dari Cloudflare R2 dan return langsung isi text-nya.
        """
        ...