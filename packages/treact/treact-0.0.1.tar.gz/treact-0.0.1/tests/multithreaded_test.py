import threading
from io import StringIO

from src.treact.renderers.console import ConsoleRenderer


def inner_fn(context):
    with context.create_node('inner_fn'):
        # print('inside inner_fn')
        context.create_node('inner_fn_child')


def test_multithreading(thread_name):
    # print(thread_name, 'start')

    buf = StringIO()
    with ConsoleRenderer() as context:
        # print(thread_name, 'inside console reader')

        with context.create_node(thread_name + 'A'):
            # print(thread_name, 'inside Node A')

            inner_fn(context)

            context.create_node(thread_name + 'B')

            with context.create_node(thread_name + 'C'):
                context.create_node(thread_name + 'D')
                # print(thread_name, 'inside Node C')
                context.create_node(thread_name + 'E')

        # print(thread_name, 'outside Node A')

    print(buf.getvalue())


t = [threading.Thread(target=test_multithreading, args=(str(i),)) for i in range(10)]

for thread in t:
    thread.start()
