import pytest
from node import paths_to_node, Node, traverse, handlers_to_node
from model import Handler, IncomingData, Writer, RouteHandler


def do_nothing(a):
    return a


def do_something(a):
    return lambda: do_nothing(a)


def test_paths_to_node():
    tests = [
        [["/"],  Node(None, do_nothing, [Node("")])],
        [["/hello"],  Node(None, do_nothing, [Node("hello")])],
        [["/", "/hello"],  Node(None, do_nothing, [Node(""), Node("hello")])],
        [["/hello", "/"],  Node(None, do_nothing, [Node(""), Node("hello")])],
        [["/", "/hello", "/goobye"],
            Node(None, do_nothing, [Node(""), Node("goobye"), Node("hello")])],
        [["/hello/user/codename"],
            Node(None, do_nothing, [Node("hello", do_nothing, [Node("user", do_nothing, [Node("codename")])])])],
        [["/", "/hello/user/codename", "zombies/tuesday", "zombies/wednesday"],
            Node(None, do_nothing, [Node(""), Node("hello", do_nothing, [Node("user", do_nothing, [Node("codename", do_nothing, [])])]), Node("zombies", do_nothing, [Node("tuesday"), Node("wednesday")])])],
        [["/", "/hello/user/codename", "zombies/tuesday", "zombies/wednesday", "zombies/wednesday/user"],
            Node(None, do_nothing, [Node(""), Node("hello", do_nothing, [Node("user", do_nothing, [Node("codename", do_nothing, [])])]), Node("zombies", do_nothing, [Node("tuesday"), Node("wednesday", do_nothing, [Node("user")])])])],
    ]

    for [path, root] in tests:
        print("TEST", path)
        got = paths_to_node(path)
        assert got == root, "test failed"


def test_traverse_node():
    tests = [
        ["/", do_something(0)],
        ["/hello/user/codename", do_something(3)],
        ["zombies/tuesday", do_something(5)],
        ["/zombies/wednesday", do_something(6)],
        ["zombies/wednesday/user", do_something(7)],
        ["zombies/other", None],
        ["/asdasdas", None],
        ["/hello/", None],
        ["/hello", None],
    ]

    root = Node(
        None, do_something(-1),
        [Node("", do_something(0)),
         Node("hello", None,
              [Node("user", None,
                    [Node("codename", do_something(3))]
                    )]),
         Node("zombies", do_something(4),
              [Node("tuesday", do_something(5)),
               Node("wednesday", do_something(6),
                    [Node("user", do_something(7))])])
         ])

    for [path, expected] in tests:
        print("TEST", path)
        got = traverse(root, path)
        if (expected == None or got == None):
            assert got == expected, "test failed"
        else:
            assert got() == expected(), "test failed"


def test_paths_to_node():
    handler = do_nothing
    tests = [
        [[RouteHandler("/", handler),
          RouteHandler("/hello/user/codename", handler),
          RouteHandler("zombies/tuesday", handler),
          RouteHandler("zombies/wednesday", handler),
          RouteHandler("zombies/wednesday/user", handler),
          ],
            Node(None, do_nothing, [Node(""), Node("hello", do_nothing, [Node("user", do_nothing, [Node("codename", do_nothing, [])])]), Node("zombies", do_nothing, [Node("tuesday"), Node("wednesday", do_nothing, [Node("user")])])])],
    ]

    for [path, root] in tests:
        print("TEST", path)
        got = handlers_to_node(path)
        assert got == root, "test failed"
