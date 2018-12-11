import numpy


class FuelGrid:

    def __init__(self, serial_number):
        self._size = 300
        self._cell_power = numpy.zeros((self._size, self._size), dtype = numpy.int)

        for i in range(self._size):
            for j in range(self._size):
                x, y = i + 1, j + 1
                rack_id = x + 10
                power = rack_id * y + serial_number
                power *= rack_id
                power = (power // 100) % 10 - 5
                self._cell_power[i, j] = power

    def cell_power(self, x, y):
        i, j = x - 1, y - 1
        return self._cell_power[i, j]

    def block_power(self, x, y, block_size):
        i, j = x - 1, y - 1
        return self._cell_power[i:i+block_size, j:j+block_size].sum()

    def max_block_power(self, block_size = 3):
        max_x, max_y, max_power = None, None, None
        for i in range(self._size - block_size + 1):
            x = i + 1
            for j in range(self._size - block_size + 1):
                y = j + 1
                power = self.block_power(x, y, block_size)
                if max_power is None or power > max_power:
                    max_x, max_y, max_power = x, y, power
        return max_x, max_y, max_power

    def max_power(self):
        max_x, max_y, max_power, max_block_size = None, None, None, None
        for block_size in range(1, self._size + 1):
            print(block_size)
            x, y, power = self.max_block_power(block_size)
            if max_power is None or power > max_power:
                max_x, max_y, max_power, max_block_size = x, y, power, block_size
        return max_x, max_y, max_power, max_block_size


def main():
    grid = FuelGrid(serial_number = 7511)
    print(grid.max_block_power())
    print(grid.max_power())


if __name__ == '__main__':
    main()
