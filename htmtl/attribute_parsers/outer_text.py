from typing import Optional

from dompa.nodes import Node, TextNode
from ..attribute_parser import AttributeParser


class OuterText(AttributeParser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "outer-text" in node.attributes:
            return TextNode(value=self.expression(node.attributes["outer-text"]))

        return node
