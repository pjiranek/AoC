from aoc import utils


class CircularList:

    class Node:

        def __init__(self, value):
            self.prev = None
            self.next = None
            self.value = value

        def node_by_offset(self, offset):
            node = self
            if offset > 0:
                for _ in range(offset):
                    node = node.next
            elif offset < 0:
                for _ in range(-offset):
                    node = node.prev
            return node

        def insert(self, value):
            new_node = type(self)(value)

            next_node = self.next

            self.next = new_node
            new_node.prev = self
            new_node.next = next_node
            next_node.prev = new_node

            return new_node

        def remove(self):
            self.prev.next, self.next.prev = self.next, self.prev

    def __init__(self, value):
        self._first = type(self).Node(value)
        self._first.prev = self._first
        self._first.next = self._first
        self._node_map = {value: self._first}

    def insert(self, pivot, offset, value):
        pivot_node = self._node_map[pivot]
        offset_node = pivot_node.node_by_offset(offset)
        new_node = offset_node.insert(value)
        self._node_map[value] = new_node

    def pop(self, pivot, offset):
        pivot_node = self._node_map[pivot]
        offset_node = pivot_node.node_by_offset(offset)
        del self._node_map[offset_node.value]
        offset_node.remove()
        return offset_node.value

    def get(self, pivot, offset):
        pivot_node = self._node_map[pivot]
        offset_node = pivot_node.node_by_offset(offset)
        return offset_node.value


class Game:

    def __init__(self, player_count):
        self._marbles = CircularList(0)
        self._current = 0

        self._player = -1
        self._player_count = player_count
        self._scores = [0] * self._player_count

        self._last = 0

    def turn(self):
        self._last += 1
        if self._last % 23 != 0:
            self._marbles.insert(self._current, 1, self._last)
            self._current = self._last
        else:
            self._scores[self._player] += self._last
            self._current = self._marbles.get(self._current, -6)
            self._scores[self._player] += self._marbles.pop(self._current, -1)

        self._player += 1
        if self._player == self._player_count:
            self._player = 0

    last = property(fget = lambda self: self._last)
    high_score = property(fget = lambda self: max(self._scores))

    def play_until(self, last_marble):
        while True:
            self.turn()
            if self._last == last_marble:
                break


def main():
    player_count, last_marble = [int(s)
                                 for s in utils.read_input('input9.txt')[0].split()
                                 if s.isdigit()]

    game = Game(player_count)
    game.play_until(last_marble)
    print(game.high_score)

    game = Game(player_count)
    game.play_until(100 * last_marble)
    print(game.high_score)


if __name__ == '__main__':
    main()
