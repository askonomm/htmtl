from typing import Optional

from dompa import Dompa
from dompa.nodes import Node, FragmentNode

from ..parser import Parser


class OuterHtml(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "outer-html" in node.attributes:
            exp = self.parse_expression(node.attributes["outer-html"])

            return FragmentNode(children=Dompa(exp).get_nodes())

        return node
