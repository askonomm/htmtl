from typing import Optional
from dompa.nodes import Node
from ..parser import Parser


class GenericValue(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        new_attrs = {}

        for key, val in node.attributes.items():
            if key.startswith(":"):
                new_attrs[key[1:]] = self.expression(val)
            else:
                new_attrs[key] = val

        node.attributes = new_attrs
        
        return node