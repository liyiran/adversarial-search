from unittest import TestCase

from hw1cs561s2018_v2 import Chess
from hw1cs561s2018_v2 import Configuration


class TestChess(TestCase):

    def test_actions(self):
        configuration1 = Configuration(path=None)
        configuration1.generate_configuration_from_string(
            """Star
MINIMAX
2
0,S1,0,0,0,0,0,0
0,0,C1,0,0,0,0,0
0,0,0,S1,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
10,20,30,40,50,60,70,80
        """)

        configuration2 = Configuration(path=None)
        configuration2.generate_configuration_from_string(
            """Circle
ALPHABETA
2
0,S2,0,0,0,0,0,0
S1,0,0,0,0,0,0,0
0,0,0,0,0,0,0,C1
0,0,0,0,0,0,S1,0
0,0,0,0,0,S1,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
10,20,30,40,50,60,70,80
            """)

        configuration3 = Configuration(path=None)
        configuration3.generate_configuration_from_string(
            """Circle
ALPHABETA
2
0,S100,0,0,0,0,0,0
0,0,C1,0,0,0,0,0
0,0,0,S1,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
10,20,30,40,50,60,70,80
            """)
        configuration4 = Configuration(path=None)
        configuration4.generate_configuration_from_string(
            """Star
ALPHABETA
2
0,C1,0,0,0,0,0,0
0,0,C1,0,0,0,0,0
0,0,0,S1,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
10,20,30,40,50,60,70,80
            """)
        chess1 = Chess(path=None, configuration=configuration1)
        chess2 = Chess(path=None, configuration=configuration2)
        chess3 = Chess(path=None, configuration=configuration3)
        chess4 = Chess(path=None, configuration=configuration4)
        self.assertEqual(2, len(chess1.actions(chess1.initial_state)))
        self.assertEqual(0, len(chess2.actions(chess2.initial_state)))
        self.assertEqual(2, len(chess3.actions(chess3.initial_state)))
        self.assertEqual(1, len(chess4.actions(chess4.initial_state)))

        self.assertEqual(80 + 60 - 20, chess1.utility(chess1.initial_state, "S"))
        self.assertEqual(80 * 2 + 70 + 50 + 40 - 30, chess2.utility(chess2.initial_state, "S"))
        self.assertEqual(80 * 100 + 60 - 20, chess3.utility(chess3.initial_state, "S"))
        self.assertEqual(60 - 10 - 20, chess4.utility(chess4.initial_state, "S"))
