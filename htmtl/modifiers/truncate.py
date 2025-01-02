from typing import Any
from ..modifier import Modifier


class Truncate(Modifier):
    def modify(self, value: Any, opts: list[Any]) -> Any:
        if isinstance(value, str) and len(opts) > 0 and isinstance(opts[0], int):
            if len(value) > opts[0]:
                return f"{value[:opts[0] - 3]}..."

        return value
