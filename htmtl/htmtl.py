from __future__ import annotations
from typing import Dict, Any, Tuple, Callable, Optional


class Node:
    name: str
    attributes: Dict[str, str]
    children: list[Node]

    def __init__(self, name: str, attributes: Dict[str, str], children: list[Node]):
        self.name = name
        self.attributes = attributes
        self.children = []


class IRBlockPosNode:
    name: str
    coords: Tuple[int, int]
    moved: bool
    children: list[IRBlockPosNode]

    def __init__(self, name: str, coords: Tuple[int, int]):
        self.name = name
        self.coords = coords


class IRBlockNode:
    name: str
    children: list[IRBlockNode]

    def __init__(self, name: str, children: list[IRBlockNode]):
        self.name = name
        self.moved = False
        self.children = children


class Htmtl:
    __template: str = ""
    __ir_block_pos_nodes: list[IRBlockPosNode] = []
    __ir_block_nodes: list[IRBlockNode] = []
    __block_elements = [
        "div", "span", "a"
    ]
    __inline_elements = [
        "img"
    ]

    def __init__(self, template: str):
        self.__template = template
        self.__ir_block_pos_nodes = []
        self.__ir_block_nodes = []
        self.__parse_ir_block_pos_nodes()
        self.__join_ir_block_pos_nodes()
        self.__parse_ir_block_nodes()

    def __parse_ir_block_pos_nodes(self):
        start = None
        end = None

        for idx, part in enumerate(self.__template):
            if part == "<":
                start = idx

            if part == ">":
                end = idx + 1

            if start is not None and end is not None:
                tag = self.__template[start:end]

                if tag.startswith("</"):
                    self.__maybe_close_ir_block_pos_node(tag, end)
                    start = None
                    end = None
                    continue

                name = tag[1:-1].split(" ")[0].strip()

                if name in self.__block_elements:
                    self.__ir_block_pos_nodes.append(
                        IRBlockPosNode(name=name, coords=(end, 0))
                    )

                start = None
                end = None

    def __maybe_close_ir_block_pos_node(self, tag: str, coord: int):
        el_name = tag[2:-1].split(' ')[0].strip()
        match = self.__find_last_match(self.__ir_block_pos_nodes, lambda node: node.name == el_name)

        if match is not None:
            [idx, last_ir_pos_node] = match
            last_ir_pos_node.coords = (last_ir_pos_node.coords[0], coord)
            self.__ir_block_pos_nodes[idx] = last_ir_pos_node

    def __join_ir_block_pos_nodes(self):
        processed_coords = set()

        for node in self.__ir_block_pos_nodes:
            if node.coords in processed_coords:
                continue

            ir_block_pos_nodes_within = self.__find_block_pos_nodes_in_coords(node.coords)
            node.children = self.__recursively_build_ir_block_pos_node_children(ir_block_pos_nodes_within, processed_coords)

        self.__ir_block_pos_nodes = [
            node for node in self.__ir_block_pos_nodes if node.coords not in processed_coords
        ]

    def __recursively_build_ir_block_pos_node_children(self, child_nodes: list[Tuple[int, IRBlockPosNode]], processed_coords: set):
        children = []

        for idx, child_node in child_nodes:
            if child_node.coords in processed_coords:
                continue

            processed_coords.add(child_node.coords)
            child_node_children = self.__find_block_pos_nodes_in_coords(child_node.coords)
            child_node.children = self.__recursively_build_ir_block_pos_node_children(child_node_children, processed_coords)
            children.append(child_node)

        return children

    def __find_block_pos_nodes_in_coords(self, coords: Tuple[int, int]) -> list[Tuple[int, IRBlockPosNode]]:
        found_block_position_nodes = []
        [start, end] = coords

        for idx, ir_block_position_node in enumerate(self.__ir_block_pos_nodes):
            [iter_start, iter_end] = ir_block_position_node.coords

            if iter_start > start and iter_end < end:
                found_block_position_nodes.append((idx, ir_block_position_node))

        return found_block_position_nodes

    def __parse_ir_block_nodes(self):
        pass

    @staticmethod
    def __find_last_match(arr: list[Any], condition: Callable[[Any], bool]) -> Optional[Tuple[int, Any]]:
        idx = len(arr)

        for item in reversed(arr):
            idx -= 1

            if condition(item):
                return idx, item

        return None

    def toHtml(self):
        pass
