import logging
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


class Node:
    def __init__(self, data, context):
        logger.debug("creating Node %s", data)
        self.data = data
        self.context = context
        self.children = []
        self.depth = 0
        self.hook_self_to_parent()

    def hook_self_to_parent(self):
        hierarchy = self.context.hierarchy
        if hierarchy:
            parent = hierarchy[-1]
            parent.add_child(self)

    def add_child(self, child):
        child.depth = self.depth + 1
        self.children.append(child)

    def __enter__(self):
        logging.debug("entering %s", self.data)
        self.context.enter(self)

    def __exit__(self, exc_type, exc_value, trace):
        logging.debug("exiting %s", self.data)
        self.context.exit(self)

    def __repr__(self):
        data = self.data
        children = self.children
        return f"Node({data=},{children=})"


@dataclass
class NodeContext:
    hierarchy: list[Node] = field(default_factory=list)
    root: Optional[Node] = None

    def create_node(self, data):
        return Node(data, self)

    def enter(self, node: Node):
        self.hierarchy.append(node)

    def exit(self, node: Node):
        if self.hierarchy:
            self.hierarchy.pop()
        self.root = node
