from collections.abc import Iterable
from typing import Optional

from dompa.nodes.actions import ToHtml
from dompa.nodes import Node, FragmentNode
from ..parser import Parser
import htmtl

class IterateOp:
    var: str
    iter_var_as: Optional[str]
    iter_index_as: Optional[str]

    def __init__(self, var: str, iter_var_as: Optional[str] = None, iter_index_as: Optional[str] = None):
        self.var = var
        self.iter_var_as = iter_var_as or None
        self.iter_index_as = iter_index_as or None


class Iterate(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "iterate" in node.attributes:
            replacement_nodes = []
            iterate_op = self.__parse_exp(node.attributes["iterate"])
            collection = self.expression(iterate_op.var)
            node.attributes.pop("iterate")

            if isinstance(collection, Iterable):
                data = self.data()

                for idx, item in enumerate(collection):
                    if iterate_op.iter_var_as:
                        data[iterate_op.iter_var_as] = item

                    if iterate_op.iter_index_as:
                        data[iterate_op.iter_index_as] = idx

                    template = htmtl.Htmtl(node.action(ToHtml), data)
                    template_nodes = template.nodes()

                    if len(template_nodes) > 0:
                        replacement_nodes.append(template_nodes[0])

            return FragmentNode(children=replacement_nodes)

        return node

    @staticmethod
    def __parse_exp(exp: str) -> IterateOp:
        parts = exp.split(" ")

        if len(parts) == 3:
            if parts[2].count(":") == 1:
                return IterateOp(
                    var=parts[0].strip(),
                    iter_index_as=parts[2].split(":")[0].strip(),
                    iter_var_as=parts[2].split(":")[1].strip()
                )

            return IterateOp(
                var=parts[0].strip(),
                iter_var_as=parts[2].strip()
            )

        return IterateOp(
            var=parts[0]
        )
