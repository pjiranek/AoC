from aoc import utils
from matplotlib import pylab


class Area:

    OPEN = '.'
    TREES = '|'
    LUMBERYARD = '#'

    height = property(fget = lambda self: self._height)
    width = property(fget = lambda self: self._width)

    def __init__(self, lines):
        self._height, self._width = len(lines), len(lines[0])
        self._grid = []
        self._counts = {Area.OPEN: 0, Area.TREES: 0, Area.LUMBERYARD: 0}
        for y, line in enumerate(lines):
            self._grid.append([])
            for char in line:
                self._grid[y].append(char)
                self._counts[char] += 1

    def __getitem__(self, key):
        x, y = key
        return self._grid[y][x]

    def __setitem__(self, key, value):
        assert value in (Area.OPEN,
                         Area.TREES,
                         Area.LUMBERYARD)

        x, y = key

        old_value = self._grid[y][x]
        self._grid[y][x] = value

        self._counts[old_value] -= 1
        self._counts[value] += 1

    def neighbors_of(self, x, y):
        neighbors = []
        for x_neigh in (x - 1, x, x + 1):
            if x_neigh not in range(self._width):
                continue
            for y_neigh in (y - 1, y, y + 1):
                if y_neigh not in range(0, self._height):
                    continue
                if x_neigh == x and y_neigh == y:
                    continue
                neighbors.append(self._grid[y_neigh][x_neigh])
        return neighbors

    def __repr__(self):
        return '\n'.join(''.join(line) for line in self._grid)

    def number_of(self, value):
        return self._counts[value]


class Simulation:

    def __init__(self, area):
        self._area = area

    def tick(self):
        new_grid = []
        for x in range(self._area.width):
            for y in range(self._area.height):
                content = self._area[x, y]
                neighbors = self._area.neighbors_of(x, y)
                if content == Area.OPEN:
                    trees = tuple(acre for acre in neighbors if acre == Area.TREES)
                    if len(trees) >= 3:
                        new_grid.append((x, y, Area.TREES))
                elif content == Area.TREES:
                    lumberyards = tuple(acre for acre in neighbors if acre == Area.LUMBERYARD)
                    if len(lumberyards) >= 3:
                        new_grid.append((x, y, Area.LUMBERYARD))
                elif content == Area.LUMBERYARD:
                    trees = tuple(acre for acre in neighbors if acre == Area.TREES)
                    lumberyards = tuple(acre for acre in neighbors if acre == Area.LUMBERYARD)
                    if len(lumberyards) >= 1 and len(trees) >= 1:
                        pass
                    else:
                        new_grid.append((x, y, Area.OPEN))

        for x, y, value in new_grid:
            self._area[x, y] = value


def main():
    lines = utils.read_input('input18.txt')
    area = Area(lines)

    simulation = Simulation(area)
    values = []
    n = 700  # This should be enough to find a period.
    for second in range(n):
        trees = area.number_of(Area.TREES)
        lumberyards = area.number_of(Area.LUMBERYARD)
        values.append(trees * lumberyards)

        simulation.tick()

    print('Part 1:', values[10])

    # Not very efficient and robust but functional period finder.
    period = 1
    while True:
        if values[-period:] == values[-2*period:-period]:
            break
        period += 1

    print(period)

    print(values[-period:][(1000000000 - n) % period])

    pylab.plot(values, 'k.')
    pylab.show()

if __name__ == '__main__':
    main()
