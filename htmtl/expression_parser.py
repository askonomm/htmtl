from typing import Any
from .modifier import Modifier


class ExpressionParser:
    __data: dict[str, Any]
    __modifiers: list[type[Modifier]]

    def __init__(self, data: dict[str, Any], modifiers: list[type[Modifier]]) -> None:
        self.__data = data
        self.__modifiers = modifiers

    def parse(self, expression: str) -> Any:
        # no curly brackets means that the whole thing is an interpolation
        if expression.count("{") == 0 and expression.count("}") == 0:
            parsed_interpolation = self.__parse_interpolation(expression)

            return parsed_interpolation

        # uneven curly brackets means invalid syntax
        if expression.count("{") != expression.count("}"):
            return expression

        # otherwise only parts of it are
        parsed_expression = ""
        interp_start = None
        interp_end = None

        for idx, char in enumerate(expression):
            parsed_expression += char

            if char == "{":
                interp_start = idx

            if char == "}":
                interp_end = idx + 1

            if interp_start is not None and interp_end is not None:
                interp = expression[interp_start:interp_end]
                parsed_interp = self.__parse_interpolation(interp[1:-1])
                parsed_expression = parsed_expression.replace(interp, parsed_interp)
                interp_start = None
                interp_end = None

        return parsed_expression

    def __parse_interpolation(self, interpolation: str) -> Any:
        parts = interpolation.split("|")
        value = self.__var_to_val(parts[0].strip())
        modifiers = [x.strip() for x in parts[1:]] if len(parts) > 1 else []

        for modifier in modifiers:
            modifier_name = ""
            args_start = None
            args_end = None
            modifier_opts = []

            for idx, char in enumerate(modifier):
                if char == "(":
                    args_start = idx + 1

                if char == ")":
                    args_end = idx

                if args_start is None and args_end is None:
                    modifier_name += char

            if args_start and args_end:
                args_str = modifier[args_start:args_end]
                modifier_opts = self.__parse_args_str_to_args(args_str)

            value = self.__modify_value(value, modifier_name, modifier_opts)

        return value

    @staticmethod
    def __parse_args_str_to_args(args_str) -> list[str | int | float | bool]:
        args = []

        for idx, char in enumerate(args_str):
            if len(args) == 0:
                args.append("")

            if char == "," and args[-1].count('"') % 2 == 0:
                args.append("")
            else:
                args[-1] += char

        parsed_args = []

        for arg in args:
            if arg.startswith("'") and arg.endswith("'"):
                parsed_args.append(arg[1:-1])
                continue

            if arg.startswith('"') and arg.endswith('"'):
                parsed_args.append(arg[1:-1])
                continue

            if all([x in "1234567890" for x in arg.lstrip("-")]):
                parsed_args.append(int(arg))
                continue

            if all([x in "1234567890." for x in arg.lstrip("-")]):
                parsed_args.append(float(arg))
                continue

            if arg == "true" or arg == "false":
                parsed_args.append(True if arg == "true" else False)

        return parsed_args

    def __modify_value(self, value: Any, modifier_name: str, modifier_opts: list[Any]) -> Any:
        for modifier in self.__modifiers:
            if modifier.__name__ == modifier_name:
                return modifier().modify(value, modifier_opts)

        return value

    def __var_to_val(self, var: str) -> Any:
        """
        Turns a expression var into the value it maps to
        in the data dictionary.
        """
        parts = var.split(".")
        value = self.__data

        for part in parts:
            if part in value:
                value = value[part]
            else:
                return None

        return value
