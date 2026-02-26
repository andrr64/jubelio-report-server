import re
from typing import Tuple, List


def bind_named_params(sql: str, params: dict) -> Tuple[str, List[str]]:
    values = []
    counter = 1

    def replacer(match):
        nonlocal counter
        key = match.group(1)

        if key not in params:
            raise ValueError(f"Missing SQL param: @{key}")

        values.append(str(params[key]))
        placeholder = f"${counter}"
        counter += 1
        return placeholder

    native_sql = re.sub(r'@(\w+)', replacer, sql)
    return native_sql, values
