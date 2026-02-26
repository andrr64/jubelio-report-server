import re

import httpx

from app.application.protocols.token_decoder_port import TokenDecoderPort
from app.application.dto.report_context import ReportContext


class TokenDecoderAdapter(TokenDecoderPort):
    # Regex untuk ambil: [key, value]Type
    PATTERN = re.compile(r'\[(?P<key>.*?),\s*(?P<value>.*?)\](?P<type>[\w\.]+)?')

    async def decode(self, token: str) -> ReportContext:
        url = f"https://report4.jubelio.com/home/dump?&token={token}"

        async with httpx.AsyncClient() as client:
            # timeout perlu agak longgar karena jubelio legacy kadang santuy
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            html_content = response.text

        matches = TokenDecoderAdapter.PATTERN.finditer(html_content)

        raw_map = {}
        # List field utama yang ada di dataclass (kecuali params)
        main_fields = {
            "reportName", "companyId", "tenantId", "logo_url", "address",
            "city", "state", "postcode", "country", "company_name", "email", "iat"
        }

        for match in matches:
            k = match.group("key").strip()
            v = match.group("value").strip()
            t = (match.group("type") or "").strip().lower()

            # 1. Handle Null/Empty
            if t == "null" or v.lower() == "null" or (not v and t != "system.string"):
                parsed_val = None

            # 2. Handle Automatic Array: [x, y, z]
            elif v.startswith('[') and v.endswith(']'):
                inner_content = v[1:-1].strip()
                if not inner_content:
                    parsed_val = []
                else:
                    # Split koma dan bersihkan whitespace
                    parsed_val = [i.strip() for i in inner_content.split(',')]

            # 3. Handle Numbers
            elif "int" in t or "long" in t:
                parsed_val = int(v) if v.isdigit() else v

            # 4. Default String
            else:
                parsed_val = v

            raw_map[k] = parsed_val

        # Pisahkan mana yang masuk field utama, mana yang masuk params
        structured_args = {k: v for k, v in raw_map.items() if k in main_fields}
        other_params = {k: v for k, v in raw_map.items() if k not in main_fields}

        return ReportContext(**structured_args, params=other_params)
