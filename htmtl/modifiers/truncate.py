from typing import Any

from ..modifier import Modifier, modifier_name


@modifier_name("truncate")
class Truncate(Modifier):
    def modify(self, value: Any, opts: list[Any]) -> Any:
        if isinstance(value, str) and len(opts) > 0:
            if all([x in "1234567890" for x in opts[0]]):
                char_limit = int(opts[0])

                if len(value) > char_limit:
                    return f"{value[:char_limit - 3]}..."

        return value
