from aoc import utils
from collections import deque


class Node:

    def __init__(self):
        self._children = []
        self._metadata = []

    children = property(fget = lambda self: self._children)
    metadata = property(fget = lambda self: self._metadata)


def make_tree(data):
    num_children = data.popleft()
    num_metadata = data.popleft()

    node = Node()
    for _ in range(num_children):
        child = make_tree(data)
        node.children.append(child)

    for _ in range(num_metadata):
        node.metadata.append(data.popleft())

    return node


def meta_sum(node):
    s = sum(node.metadata)
    for child in node.children:
        s += meta_sum(child)
    return s


def node_value(node):
    if len(node.children) == 0:
        return sum(node.metadata)
    else:
        s = 0
        for index in node.metadata:
            if 0 < index <= len(node.children):
                child = node.children[index - 1]
                s += node_value(child)
        return s


def main():
    data = deque(int(i) for i in utils.read_input('input8.txt')[0].split())
    root = make_tree(data)
    print(meta_sum(root))
    print(node_value(root))


if __name__ == '__main__':
    main()
