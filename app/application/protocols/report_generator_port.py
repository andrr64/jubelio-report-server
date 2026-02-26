from typing import Protocol, Any


class ReportGeneratorPort(Protocol):
    async def generate_xlsx(
            self,
            *,
            dsn: str,
            sql: str,
            params: list[Any],
            output_path: str
    ) -> None:
        ...
