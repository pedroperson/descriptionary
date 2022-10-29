from typing import Dict, Tuple, List, Any, Callable, Union
from dataclasses import dataclass, field
from model import Handler, IncomingData, Writer, RouteHandler

# Node stores a callback for a specific router path.
# Any valid path leads to a node that is a decendant of the root node,
# at steps of onde node per endpoint  in /endpoint/endpoint...


@dataclass
class Node:
    key: str
    callback: Handler
    children: List

    def __init__(self,
                 key: Union[str, None],
                 callback: Handler = None,
                 children: List = None):
        self.key = key
        self.callback = callback
        self.children = children if children is not None else []

    # Useful for testing so we can compare expected and generated nodes
    def __eq__(self, other):
        if not (other.key == self.key and len(other.children) == len(self.children)):
            return False

        for i, child in enumerate(other.children):
            if child != self.children[i]:
                return False

        return True


def handlers_to_node(routes: List[RouteHandler]) -> Node:
    routes = sorted(routes, key=lambda it: it.path)

    root = Node(None)
    for route in routes:
        split = clear_slash_preffix(route.path).split('/')
        node = root
        for chunk in split:
            node = append_node(node, chunk)
        node.callback = route.handler

    return root


def paths_to_node(paths: List[str]) -> Node:
    paths.sort()
    splits = [clear_slash_preffix(path).split('/') for path in paths]

    root = Node(None)
    for split in splits:
        node = root
        for chunk in split:
            node = append_node(node, chunk)

    return root


def append_node(parent: Node, key: str):
    node = Node(key)
    for child in parent.children:
        if child.key == key:
            return child

    parent.children.append(node)
    return node


#  I think it's better to just remove the first slash to not have to refuse the user their prefered style. EX: /a/b -> a/b
def clear_slash_preffix(path):
    return path[1:] if len(path) > 0 and path[0] == "/" else path


def traverse(root: Node, path: str):
    split = clear_slash_preffix(path).split('/')

    node = root
    for chunk in split:
        found = False
        for child in node.children:
            if child.key == chunk:
                found = True
                node = child
                break

        if not found:
            return None

    return node.callback
