import unittest
from aoc.y2018 import day11


class Day11Test(unittest.TestCase):

    def test_1(self):
        grid = day11.FuelGrid(serial_number = 8)
        self.assertEqual(grid.cell_power(3, 5), 4)

    def test_2(self):
        grid = day11.FuelGrid(serial_number = 57)
        self.assertEqual(grid.cell_power(122, 79), -5)

    def test_3(self):
        grid = day11.FuelGrid(serial_number = 39)
        self.assertEqual(grid.cell_power(217, 196), 0)

    def test_4(self):
        grid = day11.FuelGrid(serial_number = 71)
        self.assertEqual(grid.cell_power(101, 153), 4)

    def test_5(self):
        grid = day11.FuelGrid(serial_number = 18)
        self.assertEqual(grid.max_block_power(), (33, 45, 29))

    def test_6(self):
        grid = day11.FuelGrid(serial_number = 42)
        self.assertEqual(grid.max_block_power(), (21, 61, 30))
