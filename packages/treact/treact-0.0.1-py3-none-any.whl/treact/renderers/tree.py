from contextlib import contextmanager

from rich import print
from rich.tree import Tree

from src.treact.core import NodeContext


def render_tree(node):
    if not node:
        return
    t = Tree(node.data)
    for child in node.children:
        r = render_tree(child)
        if r:
            t.add(r)
    return t


@contextmanager
def TreeRenderer(buf=None):
    context = NodeContext()
    yield context
    print(render_tree(context.root), file=buf)
