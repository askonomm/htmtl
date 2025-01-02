from typing import Optional

from dompa import Dompa
from dompa.nodes import Node, FragmentNode

from ..parser import Parser


class OuterHtml(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "outer-html" in node.attributes:
            return FragmentNode(children=Dompa(self.expression(node.attributes["outer-html"])).nodes())

        return node