from typing import Optional
from dompa.nodes import Node
from ..parser import Parser


class WhenNot(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "when-not" in node.attributes:
            if self.parse_expression(node.attributes["when-not"]):
                return None

            node.attributes.pop("when-not")

        return node
