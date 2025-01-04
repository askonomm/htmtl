from typing import Optional
from dompa.nodes import Node
from ..parser import Parser


class When(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "when" in node.attributes:
            if not self.expression(node.attributes["when"]):
                return None

            node.attributes.pop("when")

        return node