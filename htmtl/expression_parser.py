from typing import Dict, Any, Optional

from htmtl.expression_modifier import ExpressionModifier


class ExpressionParser:
    __data: Dict[str, Any]
    __expression_modifiers: list[type[ExpressionModifier]]

    def __init__(self, data: Dict[str, Any], expression_modifiers: list[type[ExpressionModifier]]) -> None:
        self.__data = data
        self.__expression_modifiers = expression_modifiers

    def parse(self, expression: str) -> Any:
        pass

    def parse_interpolation(self, interpolation: str) -> Any:
        pass

    def use_modifier(self, value: Any, modifier_name: str, modifier_opts: list[Any]) -> Any:
        pass

    def find_modifier(self, name: str) -> Optional[ExpressionModifier]:
        pass

    def var_to_val(self, var: str) -> Any:
        pass