from aoc import utils
from collections import defaultdict
import re


def make_graph(lines):
    pattern = r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.'
    expr = re.compile(pattern)
    graph = defaultdict(lambda: {'succ': set(), 'prec': set()})
    for line in lines:
        match = expr.match(line)
        assert match
        node_from, node_to = match.groups()
        graph[node_from]['succ'].add(node_to)
        graph[node_to]['prec'].add(node_from)
    return graph


def order_nodes(graph):
    order = []
    processed = set()
    to_process = set(node for node in graph if len(graph[node]['prec']) == 0)
    while len(to_process) > 0:
        current = min(to_process)
        processed.add(current)
        to_process.remove(current)

        # Can add only successors of the current node which
        # have already processed predecessors.
        can_process_next = set(node
                               for node in graph[current]['succ']
                               if graph[node]['prec'] <= processed
                               if node not in processed)

        to_process.update(can_process_next)
        order.append(current)

    return order


def main():
    lines = utils.read_input('input7.txt')
    graph = make_graph(lines)
    order = order_nodes(graph)
    print(''.join(order))


if __name__ == '__main__':
    main()
