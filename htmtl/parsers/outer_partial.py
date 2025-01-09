from typing import Optional

from dompa import Dompa
from dompa.nodes import Node, FragmentNode

from ..parser import Parser
import htmtl


class OuterPartial(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "outer-partial" in node.attributes:
            exp = self.parse_expression(node.attributes["outer-partial"])
            template = htmtl.Htmtl(exp, self.get_data())
            replacement_nodes = Dompa(template.to_html()).get_nodes()

            return FragmentNode(children=replacement_nodes)

        return node
