from typing import Dict, Any

from .expression_modifier import ExpressionModifier


class ExpressionParser:
    __data: Dict[str, Any]
    __expression_modifiers: list[type[ExpressionModifier]]

    def __init__(self, data: Dict[str, Any], expression_modifiers: list[type[ExpressionModifier]]) -> None:
        self.__data = data
        self.__expression_modifiers = expression_modifiers

    def parse(self, expression: str) -> Any:
        # no curly brackets means that the whole thing is an interpolation
        if expression.count("{") != expression.count("}"):
            parsed_interpolation = self.__parse_interpolation(expression)

            return parsed_interpolation

        # otherwise only parts of it are
        parsed_expression = ""
        interpolation_start = None
        interpolation_end = None

        for idx, char in enumerate(expression):
            parsed_expression += char

            if char == "{":
                interpolation_start = idx

            if char == "}":
                interpolation_end = idx + 1

            if interpolation_start is not None and interpolation_end is not None:
                interpolation = expression[interpolation_start:interpolation_end]
                parsed_expression = parsed_expression.replace(interpolation, self.__parse_interpolation(interpolation[1:-1]))
                interpolation_start = None
                interpolation_end = None

        return parsed_expression

    def __parse_interpolation(self, interpolation: str) -> Any:
        parts = interpolation.split("|")
        value = self.__var_to_val(parts[0].strip())
        modifiers = [x.strip() for x in parts[1:]] if len(parts) > 1 else []

        for modifier in modifiers:
            modifier_parts = modifier.split(":")
            modifier_name = modifier_parts[0].strip()
            modifier_opts = [x.strip() for x in modifier_parts[1:]] if len(modifier_parts) > 1 else []
            value = self.__use_modifier(value, modifier_name, modifier_opts)

        return value

    def __use_modifier(self, value: Any, modifier_name: str, modifier_opts: list[Any]) -> Any:
        for modifier in self.__expression_modifiers:
            modifier_instance = modifier()

            if modifier_instance.name == modifier_name:
                return modifier_instance.modify(value, modifier_opts)

        return None

    def __var_to_val(self, var: str) -> Any:
        parts = var.split(".")
        value = self.__data

        for part in parts:
            if part in value:
                value = value[part]
            else:
                return None

        return value
