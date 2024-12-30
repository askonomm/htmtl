from typing import Any
from dompa import Dompa
from .attribute_parser import AttributeParser
from .attribute_parsers.inner_text import InnerText
from .attribute_parsers.outer_text import OuterText
from .expression_modifier import ExpressionModifier
from .expression_modifiers.truncate import Truncate
from .expression_parser import ExpressionParser


class Htmtl:
    __dom: Dompa
    __data: dict[str, Any]
    __attribute_parsers: list[type[AttributeParser]]
    __expression_modifiers: list[type[ExpressionModifier]]

    def __init__(self, template: str, data: dict[str, Any] = None):
        self.__dom = Dompa(template)
        self.__data = data or {}
        self.__attribute_parsers = self.__default_attribute_parsers()
        self.__expression_modifiers = self.__default_expression_modifiers()

    @staticmethod
    def __default_attribute_parsers() -> list[type[AttributeParser]]:
        return [
            InnerText,
            OuterText,
        ]

    @staticmethod
    def __default_expression_modifiers() -> list[type[ExpressionModifier]]:
        return [
            Truncate,
        ]

    def set_attribute_parsers(self, parsers: list[type[AttributeParser]]):
        for parser in parsers:
            if not isinstance(parser, AttributeParser):
                raise TypeError("Attribute parser must extend the AttributeParser class.")

        self.__attribute_parsers = parsers

    def set_expression_modifiers(self, modifiers: list[type[ExpressionModifier]]):
        for modifier in modifiers:
            if not isinstance(modifier, ExpressionModifier):
                raise NotImplementedError("Modifier must extend the ExpressionModifier class.")

        self.__expression_modifiers = modifiers

    def __parse(self) -> None:
        expression_parser = ExpressionParser(self.__data, self.__expression_modifiers)

        for parser in self.__attribute_parsers:
            parser_instance = parser(self.__data, expression_parser)
            self.__dom.update(parser_instance.traverse)

    def html(self) -> str:
        self.__parse()

        return self.__dom.html()