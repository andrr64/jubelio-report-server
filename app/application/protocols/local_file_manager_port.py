from typing import Protocol


class LocalFileManagerPort(Protocol):
    def create_temp_xlsx(self, report_name: str) -> str:
        ...

    def cleanup(self, path: str) -> None:
        ...
