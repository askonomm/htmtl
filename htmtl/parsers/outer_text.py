from typing import Optional

from dompa.nodes import Node, TextNode
from ..parser import Parser


class OuterText(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "outer-text" in node.attributes:
            return TextNode(value=self.expression(node.attributes["outer-text"]))

        return node
