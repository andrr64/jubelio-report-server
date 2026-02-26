# app.domain.entities.report_context
from dataclasses import dataclass, field
from typing import Optional, Any, Dict


@dataclass
class ReportContext:
    """Data yang diekstrak dari Token (Legacy/New)"""
    reportName: str
    companyId: int
    tenantId: str
    logo_url: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[str] = None
    country: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[str] = None
    iat: Optional[int] = None
    # Catch-all untuk field tambahan
    params: Dict[str, Any] = field(default_factory=dict)
