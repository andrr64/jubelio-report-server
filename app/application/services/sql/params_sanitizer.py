import json
from datetime import datetime
from typing import Dict, Any, Optional


def try_parse_date(date_str: str) -> Optional[str]:
    formats = [
        # [CRITICAL] Ini format yang muncul di log kamu (titik untuk jam)
        "%d/%m/%Y %H.%M.%S %z",

        # Format lainnya
        "%d/%m/%Y %H:%M:%S %z",
        "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S%z",  # ISO dari JWT kadang gini
        "%Y-%m-%dT%H:%M:%S.%fZ"  # ISO Standard
    ]

    for fmt in formats:
        try:
            # Parse jadi object datetime
            dt = datetime.strptime(date_str, fmt)
            # Balikin jadi ISO String yang bersih (YYYY-MM-DD HH:MM:SS+Offset)
            return dt.isoformat()
        except ValueError:
            continue
    return None


def sanitize_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Membersihkan parameter:
    1. List/Dict -> JSON String (CRITICAL untuk @brands::jsonb)
    2. Date -> ISO 8601
    3. Boolean -> 'true'/'false'
    """
    if not params:
        return {}

    cleaned_params = {}

    for key, value in params.items():
        # [PENTING] Handle tipe data List/Dict jadi JSON String
        # Contoh: value = [{'brand_id': 1}] -> "[{'brand_id': 1}]"
        if isinstance(value, (list, dict)):
            cleaned_params[key] = json.dumps(value, default=str)
            continue

        if not isinstance(value, str):
            cleaned_params[key] = value
            continue

        val = value.strip()

        if val.lower() == 'true':
            cleaned_params[key] = 'true'
            continue
        if val.lower() == 'false':
            cleaned_params[key] = 'false'
            continue

        iso_date = try_parse_date(val)
        if iso_date:
            cleaned_params[key] = iso_date
        else:
            cleaned_params[key] = val

    return cleaned_params
