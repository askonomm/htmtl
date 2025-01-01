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

    def expression(self, expression: str) -> Any:
        return self.__expression_parser.parse(expression)

    @abstractmethod
    def traverse(self, node: Node) -> Optional[Node]:
        pass