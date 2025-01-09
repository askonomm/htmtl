from typing import Any
from dompa import Dompa
from dompa.serializers import ToHtml
from dompa.nodes import Node
from .parser import Parser
from .parsers.generic_value import GenericValue
from .parsers.inner_html import InnerHtml
from .parsers.inner_partial import InnerPartial
from .parsers.inner_text import InnerText
from .parsers.iterate import Iterate
from .parsers.outer_html import OuterHtml
from .parsers.outer_partial import OuterPartial
from .parsers.outer_text import OuterText
from .parsers.when import When
from .parsers.when_not import WhenNot
from .modifier import Modifier
from .modifiers.truncate import Truncate
from .expression_parser import ExpressionParser


class Htmtl:
    __dom: Dompa
    __data: dict[str, Any]
    __parsers: list[type[Parser]]
    __modifiers: list[type[Modifier]]

    def __init__(self, template: str, data: dict[str, Any] = None):
        self.__dom = Dompa(template)
        self.__data = data or {}

        # set default attribute parsers
        self.__parsers = [
            Iterate,
            InnerText,
            InnerHtml,
            InnerPartial,
            OuterText,
            OuterHtml,
            OuterPartial,
            GenericValue,
            When,
            WhenNot,
        ]

        # set default expression modifiers
        self.__modifiers = [
            Truncate,
        ]

    def set_parsers(self, parsers: list[type[Parser]]):
        for parser in parsers:
            if not isinstance(parser, Parser):
                raise TypeError("Parser must extend the Parser class.")

        self.__parsers = parsers

    def set_modifiers(self, modifiers: list[type[Modifier]]):
        for modifier in modifiers:
            if not isinstance(modifier, Modifier):
                raise NotImplementedError("Modifier must extend the Modifier class.")

        self.__modifiers = modifiers

    def __parse(self) -> None:
        expression_parser = ExpressionParser(self.__data, self.__modifiers)

        for parser in self.__parsers:
            parser_instance = parser(self.__data, expression_parser)
            self.__dom.traverse(parser_instance.traverse)

    def to_html(self) -> str:
        """
        Conver the template into HTML.
        """
        self.__parse()

        return self.__dom.serialize(ToHtml)

    def get_nodes(self) -> list[Node]:
        """
        Return the node tree representation of the template.
        """
        self.__parse()

        return self.__dom.get_nodes()
