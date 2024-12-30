from dompa.nodes import Node, TextNode
from htmtl.attribute_parser import AttributeParser


class InnerText(AttributeParser):
    def traverse(self, node: Node):
        if "inner-text" in node.attributes:
            node.children = [TextNode(self.expression(node.attributes["inner-text"]))]
            node.attributes.pop("inner-text")