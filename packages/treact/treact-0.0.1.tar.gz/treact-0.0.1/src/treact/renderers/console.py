import pprint
from contextlib import contextmanager

from src.treact.core import NodeContext


@contextmanager
def ConsoleRenderer(buf=None):
    context = NodeContext()
    yield context
    pprint.pprint(context.root, indent=4, stream=buf)
