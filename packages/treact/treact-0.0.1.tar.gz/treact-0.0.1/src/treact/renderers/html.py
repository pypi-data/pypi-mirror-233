from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional
from xml.dom.minidom import Document, Node as DomNode

from src.treact.core import Node, NodeContext


@dataclass
class HtmlElement:
    tag: str
    attrs: dict[str, str]


class HtmlNode(Node):
    def __call__(self, *args, **kwargs):
        self.data.attrs.update(kwargs)
        return self


class HtmlNodeContext(NodeContext):
    def create_node(self, data):
        return HtmlNode(data, self)

    def html_node(self, tag: str, attrs: dict[str, str] | None = None):
        if attrs is None:
            attrs = {}
        return self.create_node(HtmlElement(tag, attrs))

    def text_node(self, text: str):
        return self.create_node(text)

    def __getattr__(self, tag_name: str):
        return self.html_node(tag_name)


def render_html(node: Optional[Node], document=Document()) -> Optional[DomNode]:
    if not node:
        return

    if isinstance(node.data, str):
        return document.createTextNode(node.data)

    tag_name = node.data.tag

    element = document.createElement(tag_name)
    for key, value in node.data.attrs.items():
        element.setAttribute(key, value)
    for child in node.children:
        element.appendChild(render_html(child, document))
    return element


@contextmanager
def HtmlRenderer(buf=None):
    context = HtmlNodeContext()
    yield context
    print('<!DOCTYPE html>', file=buf)
    print(render_html(context.root).toprettyxml(), file=buf)
