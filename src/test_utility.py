from unittest import TestCase

from hw1cs561s2018 import Board
from hw1cs561s2018 import Configuration
from hw1cs561s2018 import Utility


class TestUtility(TestCase):
    configuration = Configuration(path=None)
    configuration.player = "S"
    configuration.row_values = [10, 20, 30, 40, 50, 60, 70, 80]

    def test_evaluation1(self):
        board = Board(pieces=None, map=[
            ['0', 'S1', '0', '0', '0', '0', '0', '0'],
            ['0', '0', 'C1', '0', '0', '0', '0', '0'],
            ['0', '0', '0', 'S1', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0']
        ])
        utility = board.evaluation(self.configuration, None)
        self.assertEqual(120, utility)
        s1 = [x for x in board.pieces if x.coor == (0, 1)]
        c1 = [x for x in board.pieces if x.coor == Utility.right_down(s1[0].coor)]
        self.assertEqual((1, 2), c1[0].coor)
        action_list = Utility.action(board, "S")
        self.assertEqual(2, len(action_list))

    def test_evaluation2(self):
        board = Board(pieces=None, map=[
            ['0', 'S2', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0']
        ])
        utility = board.evaluation(self.configuration, None)
        self.assertEqual(160, utility)
        s1 = [x for x in board.pieces if x.coor == (0, 1)]
        self.assertEqual("0", board.map[Utility.right_down(s1[0].coor)[0]][Utility.right_down(s1[0].coor)[1]])
        action_list = Utility.action(board, "S")
        self.assertEqual(0, len(action_list))

    def test_evaluation3(self):
        board = Board(pieces=None, map=[
            ['0', 'S2', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', 'C1'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0']
        ])
        utility = board.evaluation(self.configuration, None)
        self.assertEqual(130, utility)
        action_list = Utility.action(board, "S")
        self.assertEqual(0, len(action_list))

    def test_evaluation3_1(self):
        board = Board(pieces=None, map=[
            ['0', 'S2', '0', '0', '0', '0', '0', '0'],
            ['S1', '0', 'C1', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', 'C1'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0']
        ])
        utility = board.evaluation(self.configuration, None)
        self.assertEqual(160 + 70 - 20 - 30, utility)
        action_list = Utility.action(board, "S")
        self.assertEqual(1, len(action_list))

    def test_evaluation4(self):
        config = Configuration(path=None)
        config.player = "C"
        config.row_values = [10, 20, 30, 40, 50, 60, 70, 80]
        board = Board(pieces=None, map=[
            ['0', 'S2', '0', '0', '0', '0', '0', '0'],
            ['S1', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', 'C1'],
            ['0', '0', '0', '0', '0', '0', 'S1', '0'],
            ['0', '0', '0', '0', '0', 'S1', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0']
        ])
        utility = board.evaluation(config, None)
        self.assertEqual(-290, utility)
        action_list = Utility.action(board, "S")
        self.assertEqual(3, len(action_list))

    def test_evaluation5(self):
        config = Configuration(path=None)
        config.player = "S"
        config.row_values = [10, 20, 30, 40, 52, 70, 90, 1000]
        board = Board(pieces=None, map=[
            ['0', 'C1', '0', 'C1', '0', 'C1', '0', 'C1'],  # 10
            ['C1', '0', 'C1', '0', 'C1', '0', 'C1', '0'],  # 20
            ['0', 'S1', '0', 'S1', '0', 'S1', '0', 'S1'],  # 30
            ['S1', '0', 'S1', '0', 'S1', '0', 'S1', '0'],  # 40
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0']
        ])
        utility = board.evaluation(config, None)
        self.assertEqual(368, utility)
        action_list = Utility.action(board, "S")
        self.assertEqual(0, len(action_list))
