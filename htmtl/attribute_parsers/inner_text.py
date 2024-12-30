from typing import Optional

from dompa.nodes import Node, TextNode
from ..attribute_parser import AttributeParser


class InnerText(AttributeParser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "inner-text" in node.attributes:
            node.children = [TextNode(value=self.expression(node.attributes["inner-text"]))]
            node.attributes.pop("inner-text")

        return node