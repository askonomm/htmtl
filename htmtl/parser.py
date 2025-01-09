from abc import ABC, abstractmethod
from typing import Any, Optional
from dompa.nodes import Node
from .expression_parser import ExpressionParser


class Parser(ABC):
    __data: dict[str, Any]
    __expression_parser: ExpressionParser

    def __init__(self, data: dict[str, Any], expression_parser: ExpressionParser) -> None:
        self.__data = data
        self.__expression_parser = expression_parser

    def get_data(self) -> dict[str, Any]:
        """
        Return the data dictionary.
        """
        return self.__data

    def parse_expression(self, expression: str) -> Any:
        """
        Parses a given expression.
        """
        return self.__expression_parser.parse(expression)

    @abstractmethod
    def traverse(self, node: Node) -> Optional[Node]:
        pass
