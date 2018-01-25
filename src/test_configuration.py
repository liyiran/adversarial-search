from unittest import TestCase

from hw1cs561s2018 import Configuration
from hw1cs561s2018 import Piece


class TestConfiguration(TestCase):
    def test_hello(self):
        self.assertTrue(True)

    def test_read_file1(self):
        configuration = Configuration("../res/test_case_1.txt")
        self.assertEqual(configuration.player, "S")
        self.assertEqual(configuration.algorithm, "MINIMAX")
        self.assertEqual(configuration.depth_limit, 2)
        self.assertEqual(configuration.row_values, [10, 20, 30, 40, 50, 60, 70, 80])
        # self.assertEqual(configuration.initial_state,[['0','S1','0','0','0','0','0','0'],
        #                                               ['0','0','C1','0','0','0','0','0'],
        #                                               ['0','0','0','S1','0','0','0','0'],
        #                                               ['0','0','0','0','0','0','0','0'],
        #                                               ['0','0','0','0','0','0','0','0'],
        #                                               ['0','0','0','0','0','0','0','0'],
        #                                               ['0','0','0','0','0','0','0','0'],
        #                                               ['0','0','0','0','0','0','0','0']])
        board = configuration.initial_state
        self.assertEqual(board.map, [['0', 'S1', '0', '0', '0', '0', '0', '0'],
                                     ['0', '0', 'C1', '0', '0', '0', '0', '0'],
                                     ['0', '0', '0', 'S1', '0', '0', '0', '0'],
                                     ['0', '0', '0', '0', '0', '0', '0', '0'],
                                     ['0', '0', '0', '0', '0', '0', '0', '0'],
                                     ['0', '0', '0', '0', '0', '0', '0', '0'],
                                     ['0', '0', '0', '0', '0', '0', '0', '0'],
                                     ['0', '0', '0', '0', '0', '0', '0', '0']])
        self.assertEqual(len(board.pieces), 3)
        piece1 = Piece("S", (0, 1))
        piece2 = Piece("S", (2, 3))
        piece3 = Piece("C", (1, 2))
        self.assertTrue(piece1 in board.pieces)
        self.assertTrue(piece2 in board.pieces)
        self.assertTrue(piece3 in board.pieces)

    def test_read_file2(self):
        configuration = Configuration("../res/test_case_2.txt")
        self.assertEqual(configuration.player, "C")
        self.assertEqual(configuration.algorithm, "ALPHABETA")
        self.assertEqual(configuration.depth_limit, 2)
        self.assertEqual(configuration.row_values, [10, 20, 30, 40, 50, 60, 70, 80])
        self.assertEqual(len(configuration.initial_state.pieces), 6)
        piece1 = Piece("S", (0, 1))
        piece2 = Piece("S", (1, 0))
        piece3 = Piece("C", (2, 7))
        piece4 = Piece("S", (3, 6))
        piece5 = Piece("S", (4, 5))
        self.assertEqual(configuration.initial_state.pieces.count(piece1), 2)
        self.assertTrue(piece2 in configuration.initial_state.pieces)
        self.assertTrue(piece3 in configuration.initial_state.pieces)
        self.assertTrue(piece4 in configuration.initial_state.pieces)
        self.assertTrue(piece5 in configuration.initial_state.pieces)
