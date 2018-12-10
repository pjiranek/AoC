import unittest
from aoc.y2018 import day9


class Day9Test(unittest.TestCase):

    def test_1(self):
        self._do_test(10, 1618, 8317)

    def test_2(self):
        self._do_test(13, 7999, 146373)

    def test_3(self):
        self._do_test(17, 1104, 2764)

    def test_4(self):
        self._do_test(21, 6111, 54718)

    def test_5(self):
        self._do_test(30, 5807, 37305)

    def _do_test(self, player_count, last_marble, high_score):
        game = day9.Game(player_count)
        game.play_until(last_marble)
        self.assertEqual(game.high_score, high_score)
