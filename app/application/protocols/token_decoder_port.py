from typing import Protocol

from app.application.dto.report_context import ReportContext


class TokenDecoderPort(Protocol):
    async def decode(self, token: str) -> ReportContext:
        """Semua jenis decoder wajib punya fungsi ini"""
        pass
