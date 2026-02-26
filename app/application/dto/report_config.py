from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ReportConfig:
    report_name: str
    query: str
    params: Dict[str, Any]
