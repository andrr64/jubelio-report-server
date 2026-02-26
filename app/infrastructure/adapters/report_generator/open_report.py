import re
from datetime import datetime, date, time
from decimal import Decimal
from typing import Any, Dict, List
from uuid import UUID

import psycopg
import xlsxwriter
from psycopg.rows import dict_row

from app.application.protocols.report_generator_port import ReportGeneratorPort

_ILLEGAL_XML_RE = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")
_EXCEL_CELL_STR_LIMIT = 32767


def _safe_str(s: str) -> str:
    if not s:
        return ""
    s = _ILLEGAL_XML_RE.sub("", s)
    if len(s) > _EXCEL_CELL_STR_LIMIT:
        s = s[:_EXCEL_CELL_STR_LIMIT]
    return s


def _to_text(val: Any) -> str:
    # semua yang non-numeric kita jadikan text stabil
    if val is None:
        return ""
    if isinstance(val, datetime):
        return val.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(val, date) and not isinstance(val, datetime):
        return val.strftime("%Y-%m-%d")
    if isinstance(val, time):
        return val.strftime("%H:%M:%S")
    if isinstance(val, (Decimal, UUID)):
        return str(val)
    return str(val)


def get_report_generator():
    return OpenReportAdapter()


class OpenReportAdapter(ReportGeneratorPort):
    async def generate_xlsx(
            self,
            *,
            dsn: str,
            sql: str,
            params: list[Any],
            output_path: str
    ) -> None:

        psycopg_sql = re.sub(r"\$\d+", "%s", sql)

        # 🔥 KUNCI FIX: matikan strings_to_formulas + strings_to_urls
        workbook = xlsxwriter.Workbook(
            output_path,
            {
                "constant_memory": True,
                "remove_timezone": True,
                "strings_to_formulas": False,
                "strings_to_urls": False,
            },
        )
        worksheet = workbook.add_worksheet("Report")

        state = {"row_num": 0, "headers": []}

        try:
            async with await psycopg.AsyncConnection.connect(dsn, autocommit=True) as conn:
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute(psycopg_sql, params)

                    while True:
                        batch = await cur.fetchmany(2000)
                        if not batch:
                            break

                        # ✅ tulis langsung (xlsxwriter tidak thread-safe)
                        self._write_batch_sync(worksheet, batch, state)

            if state["row_num"] == 0:
                worksheet.write_string(0, 0, "No Data Found")

        finally:
            workbook.close()

    def _write_batch_sync(self, worksheet, batch: List[Dict], state: dict):
        for row_data in batch:
            if state["row_num"] == 0:
                state["headers"] = list(row_data.keys())
                for col_num, header in enumerate(state["headers"]):
                    worksheet.write_string(0, col_num, _safe_str(str(header)))
                state["row_num"] = 1

            r = state["row_num"]

            for c, header in enumerate(state["headers"]):
                val = row_data.get(header)

                # angka & boolean biar tetap angka/boolean
                if isinstance(val, bool):
                    worksheet.write_boolean(r, c, val)
                elif isinstance(val, (int, float)) and val is not None:
                    worksheet.write_number(r, c, float(val) if isinstance(val, Decimal) else val)
                else:
                    # 🔥 semua selain numeric dipaksa TEXT (anti formula)
                    s = _safe_str(_to_text(val))
                    worksheet.write_string(r, c, s)

            state["row_num"] += 1
