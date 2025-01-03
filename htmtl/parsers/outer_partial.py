from typing import Optional

from dompa import Dompa
from dompa.nodes import Node, FragmentNode

from ..parser import Parser
import htmtl

class OuterPartial(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "outer-partial" in node.attributes:
            template = htmtl.Htmtl(self.expression(node.attributes["outer-partial"]), self.data())
            replacement_nodes = Dompa(template.html()).nodes()

            return FragmentNode(children=replacement_nodes)

        return node