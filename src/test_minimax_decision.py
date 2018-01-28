from unittest import TestCase

from hw1cs561s2018 import Board


class TestMinimax_decision(TestCase):
    def test_minimax_decision(self):
        board = Board(pieces=None, map=[
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', 'S1', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0']
        ])
        # chess = Chess("../res/test_case_1.txt")
        # value = minimax_decision(state=chess.initial, game=chess)
        # self.assertEqual(80, value)
