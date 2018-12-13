from aoc import utils
import collections


class Map:

    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4
    VERTICAL = 5
    HORIZONTAL = 6
    INTERSECTION = 7

    def __init__(self, lines):
        self._height, self._width = len(lines), max(len(line) for line in lines)

        self._grid = []
        for _ in range(self._height):
            self._grid.append([None] * self._width)

        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char != ' ':
                    self._grid[row][col] = char

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == '/':
                    top, bottom, left, right = self._get_track_rectangle(row, col)

                    self._grid[top][left] = self.TOP_LEFT
                    self._grid[top][right] = self.TOP_RIGHT
                    self._grid[bottom][left] = self.BOTTOM_LEFT
                    self._grid[bottom][right] = self.BOTTOM_RIGHT

                    self._outline_rectangle(top, bottom, left, right)

    def _get_track_rectangle(self, row, col):
        assert self._grid[row][col] == '/'

        top, left = row, col
        bottom, right = None, None

        for col in range(left + 1, self._width):
            if self._grid[top][col] == '\\':
                right = col
                break

        for row in range(top + 1, self._height):
            if self._grid[row][right] == '/':
                bottom = row
                break

        return top, bottom, left, right

    def _outline_rectangle(self, top, bottom, left, right):
        for col in range(left + 1, right):
            self._grid[top][col] = self.HORIZONTAL if self._grid[top][col] != self.VERTICAL else self.INTERSECTION
            self._grid[bottom][col] = self.HORIZONTAL if self._grid[bottom][col] != self.VERTICAL else self.INTERSECTION
        for row in range(top + 1, bottom):
            self._grid[row][left] = self.VERTICAL if self._grid[row][left] != self.HORIZONTAL else self.INTERSECTION
            self._grid[row][right] = self.VERTICAL if self._grid[row][right] != self.HORIZONTAL else self.INTERSECTION

    @staticmethod
    def cell_str(cell):
        return {None: ' ',
                Map.TOP_LEFT: '┌',
                Map.TOP_RIGHT: '┐',
                Map.BOTTOM_LEFT: '└',
                Map.BOTTOM_RIGHT: '┘',
                Map.VERTICAL: '│',
                Map.HORIZONTAL: '─',
                Map.INTERSECTION: '┼'}[cell]

    def __repr__(self):
        return '\n'.join((''.join(self.cell_str(c) for c in line)) for line in self._grid)

    height = property(fget = lambda self: self._height)
    width = property(fget = lambda self: self._width)

    def __getitem__(self, item):
        return self._grid[item[0]][item[1]]


class Cart:

    DIRECTION_RIGHT = 0
    DIRECTION_UP = 1
    DIRECTION_LEFT = 2
    DIRECTION_DOWN = 3

    NEXT_LEFT = 1
    NEXT_STRAIGHT = 0
    NEXT_RIGHT = -1

    _corner_turns = {Map.TOP_LEFT:     {DIRECTION_UP:   -1, DIRECTION_LEFT:  +1},
                     Map.TOP_RIGHT:    {DIRECTION_UP:   +1, DIRECTION_RIGHT: -1},
                     Map.BOTTOM_LEFT:  {DIRECTION_DOWN: +1, DIRECTION_LEFT:  -1},
                     Map.BOTTOM_RIGHT: {DIRECTION_DOWN: -1, DIRECTION_RIGHT: +1}}

    def __init__(self, row, col, direction, map):
        self._row = row
        self._col = col
        self._direction = direction
        self._map = map

        self._next = self.NEXT_LEFT

    row = property(fget = lambda self: self._row)
    col = property(fget = lambda self: self._col)
    direction = property(fget = lambda self: self._direction)

    def advance(self):
        self._row += (self._direction % 2) * (self._direction - 2)
        self._col += ((self._direction + 1) % 2) * (1 - self._direction)

        cell = self._map[self._row, self._col]
        if cell == Map.INTERSECTION:
            self._direction += self._next
            self._next -= 1
            self._next = (self._next + 1) % 3 - 1
        elif cell in (Map.TOP_LEFT, Map.TOP_RIGHT, Map.BOTTOM_LEFT, Map.BOTTOM_RIGHT):
            self._direction += Cart._corner_turns[cell][self._direction]
        self._direction %= 4

    def __repr__(self):
        return {self.DIRECTION_UP: '▲',
                self.DIRECTION_DOWN: '▼',
                self.DIRECTION_LEFT: '◀',
                self.DIRECTION_RIGHT: '▶'}[self._direction]

    def __lt__(self, other):
        return (self.row, self.col) < (other.row, other.col)


class CrashException(BaseException):

    def __init__(self, row, col, carts):
        self._row = row
        self._col = col
        self._carts = tuple(carts)

    row = property(fget = lambda self: self._row)
    col = property(fget = lambda self: self._col)
    carts = property(fget = lambda self: self._carts)


class Traffic:

    def __init__(self, map, lines):
        assert isinstance(map, Map)

        self._map = map

        self._carts = []
        self._cart_grid = collections.defaultdict(lambda: set())

        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char in ('v', '^', '<', '>'):
                    direction = {'^': Cart.DIRECTION_UP,
                                 'v': Cart.DIRECTION_DOWN,
                                 '<': Cart.DIRECTION_LEFT,
                                 '>': Cart.DIRECTION_RIGHT}[char]
                    cart = Cart(row, col, direction, self._map)
                    self._carts.append(cart)
                    self._cart_grid[row, col].add(cart)

        self._unprocessed = None

    def __repr__(self):
        lines = []
        for row in range(self._map.height):
            line = []
            for col in range(self._map.width):
                line.append(Map.cell_str(self._map[row, col]))
            lines.append(line)

        for cart in self._carts:
            lines[cart.row][cart.col] = repr(cart)

        return '\n'.join(''.join(c for c in line) for line in lines)

    def tick(self):
        if self.tick_finished:
            self._unprocessed = collections.deque(sorted(self._carts))

        while not self.tick_finished:
            cart = self._unprocessed.popleft()
            self._cart_grid[cart.row, cart.col].remove(cart)

            cart.advance()
            self._cart_grid[cart.row, cart.col].add(cart)

            if len(self._cart_grid[cart.row, cart.col]) > 1:
                raise CrashException(cart.row, cart.col, self._cart_grid[cart.row, cart.col])

    def remove(self, cart):
        self._carts.remove(cart)
        self._cart_grid[cart.row, cart.col].remove(cart)
        if self._unprocessed is not None and cart in self._unprocessed:
            self._unprocessed.remove(cart)

    carts = property(fget = lambda self: self._carts)
    tick_finished = property(fget = lambda self: self._unprocessed is None or len(self._unprocessed) == 0)


def main():
    lines = utils.read_input('input13.txt')

    map = Map(lines)
    traffic = Traffic(map, lines)

    while True:
        try:
            while True:
                traffic.tick()
        except CrashException as crash:
            print('Crash at ({0},{1})'.format(crash.col, crash.row))
            for cart in crash.carts:
                traffic.remove(cart)
            if len(traffic.carts) == 1:
                if not traffic.tick_finished:
                    traffic.tick()
                print('Last standing cart at ({0},{1})'.format(traffic.carts[0].col, traffic.carts[0].row))
                break


if __name__ == '__main__':
    main()
