from typing import Optional

from dompa.nodes import Node, TextNode
from ..parser import Parser


class InnerText(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "inner-text" in node.attributes:
            exp = self.parse_expression(node.attributes["inner-text"])
            node.children = [TextNode(value=exp)]
            node.attributes.pop("inner-text")

        return node
