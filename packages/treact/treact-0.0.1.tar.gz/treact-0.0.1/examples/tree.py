from src.treact.renderers.tree import TreeRenderer


def component(name, context):
    with context.create_node(f"My comp {name}"):
        context.create_node("Text")


def container_wrapper(name, context):
    n = context.create_node(f"My wrapper comp {name}")
    with n:
        component(name, context)
    return n


def tree(context):
    with context.create_node("Root"):
        with context.create_node("A"):
            component("123", context)
            context.create_node("B")
            with context.create_node("C"):
                context.create_node("D")
        context.create_node("E")
        component("456", context)
        for i in range(3):
            context.create_node(f"iter {i}")
        with context.create_node("F"):
            context.create_node("G")
        with container_wrapper("test", context):
            context.create_node("under test")


with TreeRenderer() as context:
    tree(context)
