from abc import ABC, abstractmethod
from typing import Any, Dict
from dompa.nodes import Node

from htmtl.expression_parser import ExpressionParser


class AttributeParser(ABC):
    __data: Dict[str, Any]
    __expression_parser: ExpressionParser

    def __init__(self, data: Dict[str, Any], expression_parser: ExpressionParser) -> None:
        self.__data = data
        self.__expression_parser = expression_parser

    def expression(self, expression: str) -> Any:
        return self.__expression_parser.parse(expression)

    @abstractmethod
    def traverse(self, node: Node):
        pass