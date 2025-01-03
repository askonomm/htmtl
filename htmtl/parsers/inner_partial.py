from typing import Optional

from dompa import Dompa
from dompa.nodes import Node

from ..parser import Parser
import htmtl

class InnerPartial(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "inner-partial" in node.attributes:
            template = htmtl.Htmtl(self.expression(node.attributes["inner-partial"]), self.data())
            child_nodes = Dompa(template.html()).nodes()
            node.children = child_nodes
            node.attributes.pop("inner-partial")

        return node