from typing import Optional

from dompa import Dompa
from dompa.nodes import Node

from ..parser import Parser


class InnerHtml(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "inner-html" in node.attributes:
            exp = self.parse_expression(node.attributes["inner-html"])
            child_nodes = Dompa(exp).get_nodes()
            node.children = child_nodes
            node.attributes.pop("inner-html")

        return node
