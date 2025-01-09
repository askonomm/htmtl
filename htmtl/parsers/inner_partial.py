from typing import Optional

from dompa import Dompa
from dompa.nodes import Node

from ..parser import Parser
import htmtl


class InnerPartial(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "inner-partial" in node.attributes:
            exp = self.parse_expression(node.attributes["inner-partial"])
            template = htmtl.Htmtl(exp, self.get_data())
            child_nodes = Dompa(template.to_html()).get_nodes()
            node.children = child_nodes
            node.attributes.pop("inner-partial")

        return node
