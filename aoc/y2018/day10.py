from aoc import utils
from scipy.sparse import coo_matrix
from matplotlib import pylab
import re
import numpy


class MovingImage:

    def __init__(self):
        lines = utils.read_input('input10.txt')
        num_points = len(lines)

        self._x = numpy.zeros(num_points, dtype = numpy.int)
        self._y = numpy.zeros(num_points, dtype = numpy.int)
        self._vx = numpy.zeros(num_points, dtype = numpy.int)
        self._vy = numpy.zeros(num_points, dtype = numpy.int)

        expr = re.compile(r'^position=<(.*)> velocity=<(.*)>$')
        for i, line in enumerate(lines):
            match = expr.match(line)
            position = [i for i in match.groups()[0].split(',')]
            velocity = [int(i) for i in match.groups()[1].split(',')]
            self._x[i], self._y[i] = position
            self._vx[i], self._vy[i] = velocity

        self._step_count = 0

    step_count = property(fget = lambda self: self._step_count)

    def advance(self, n = 1):
        for _ in range(n):
            self._x += self._vx
            self._y += self._vy
            self._step_count += 1

    @property
    def group_count(self):

        def remove_connected(points, ref):
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if i == j == 0:
                        continue
                    p = (ref[0] + i, ref[1] + j)
                    if p in points:
                        points.remove(p)
                        remove_connected(points, p)

        points = set((x, y) for x, y in zip(self._x, self._y))
        count = 0
        while len(points) > 0:
            start = points.pop()
            remove_connected(points, start)
            count += 1

        return count

    def plot(self):
        matrix = coo_matrix((numpy.ones(len(self._x)), (self._y - self._y.min(), self._x - self._x.min())))
        pylab.spy(matrix)
        pylab.show()


def main():
    image = MovingImage()
    while image.group_count > 8:
        image.advance()
    print(image.step_count)
    image.plot()


if __name__ == '__main__':
    main()
