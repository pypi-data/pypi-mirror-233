from src.treact.renderers.html import HtmlRenderer


def component(name, c):
    with c.pre:
        context.text_node('#' * (len(name) + 6))
        context.text_node(f"# {name} #")
        context.text_node('#' * (len(name) + 6))


def container(c):
    return c.div(style="border: 1px solid black")


styles = """
button {
    background-color: red;
}
"""


def ui(c):
    with c.html:
        with c.head:
            with c.title:
                c.text_node("Hello world")

            with c.style:
                c.text_node(styles)

        with c.body:
            with c.button(onclick="alert('hello')"):
                c.text_node("Click me")

            with c.ol:
                for i in range(3):
                    with c.li:
                        c.text_node(f"list item {i}")

            component("hello components 👋", c)

            with container(c):
                component("look ma, i m trapped in a container", c)


with HtmlRenderer() as context:
    ui(context)
