import os
import uuid

from app.application.protocols.local_file_manager_port import LocalFileManagerPort


class LocalFileManagerAdapter(LocalFileManagerPort):
    BASE_DIR = "temp_reports"

    def create_temp_xlsx(self, report_name: str) -> str:
        os.makedirs(self.BASE_DIR, exist_ok=True)
        filename = f"{report_name}_{uuid.uuid4().hex}.xlsx"
        return os.path.join(self.BASE_DIR, filename)

    def cleanup(self, path: str) -> None:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(e)
