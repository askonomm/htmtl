from typing import Optional

from dompa.nodes import Node, TextNode
from ..parser import Parser


class OuterText(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "outer-text" in node.attributes:
            exp = self.parse_expression(node.attributes["outer-text"])

            return TextNode(value=exp)

        return node
