from typing import Optional

from dompa import Dompa
from dompa.nodes import Node

from ..parser import Parser


class InnerHtml(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "inner-html" in node.attributes:
            child_nodes = Dompa(self.expression(node.attributes["inner-html"])).nodes()
            node.children = child_nodes
            node.attributes.pop("inner-html")

        return node