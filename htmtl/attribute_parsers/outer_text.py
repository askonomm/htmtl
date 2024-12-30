from dompa.nodes import Node, TextNode
from ..attribute_parser import AttributeParser


class OuterText(AttributeParser):
    def traverse(self, node: Node):
        if "outer-text" in node.attributes:
            node.replace_with(TextNode(value=self.expression(node.attributes["outer-text"])))
