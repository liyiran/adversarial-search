from unittest import TestCase

from hw1cs561s2018_v2 import Chess
from hw1cs561s2018_v2 import Configuration
from hw1cs561s2018_v2 import minimax_decision


class TestChess(TestCase):
    def test_evaluation(self):
        configuration2 = Configuration(path=None)
        configuration2.generate_configuration_from_string(
            """Circle
ALPHABETA
2
0,S3,0,0,0,0,0,S1
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,C1,0
10,20,30,40,50,60,70,80
            """)
        chess2 = Chess(path=None, configuration=configuration2)
        self.assertEqual(80 - 4 * 80, chess2.evaluation(chess2.initial_state.pieces, "C", configuration2.row_values))

    ############################################################
    def test_action_no_action(self):
        configuration1 = Configuration(path=None)
        configuration1.generate_configuration_from_string(
            """Star
MINIMAX
2
0,S1,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,S1,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
10,20,30,40,50,60,70,80
        """)
        chess1 = Chess(path=None, configuration=configuration1)
        utility1 = minimax_decision(chess1.initial_state, chess1)
        self.assertEqual(140, utility1)

    #############################################
    def test_action_go_to_boarder(self):
        configuration1 = Configuration(path=None)
        configuration1.generate_configuration_from_string(
            """Circle
MINIMAX
2
0,S2,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,C1
0,0,0,0,0,0,S1,0
0,0,0,0,0,S1,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
10,20,30,40,50,60,70,80
        """)
        chess1 = Chess(path=None, configuration=configuration1)
        utility1 = minimax_decision(chess1.initial_state, chess1)
        self.assertEqual(2 * 80 + 2 * 60, -utility1)

    #####################
    def test_action_go_to_boarder1(self):
        configuration1 = Configuration(path=None)
        configuration1.generate_configuration_from_string(
            """Circle
MINIMAX
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
        chess1 = Chess(path=None, configuration=configuration1)
        utility1 = minimax_decision(chess1.initial_state, chess1)
        self.assertEqual(2 * 80 + 2 * 60 + 80, -utility1)

    def test_action_go_to_boarder4(self):
        configuration1 = Configuration(path=None)
        configuration1.generate_configuration_from_string(
            """Star
MINIMAX
2
0,C1,0,0,0,0,0,S1
C1,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
10,20,30,40,50,60,70,80
    """)
        chess1 = Chess(path=None, configuration=configuration1)
        utility1 = minimax_decision(chess1.initial_state, chess1)
        self.assertEqual(80, -utility1)

    ########################################
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
        actions1 = chess1.actions(chess1.initial_state)
        self.assertEqual(2, len(actions1))
        actions2 = chess2.actions(chess2.initial_state)
        self.assertEqual(1, len(actions2))
        actions3 = chess3.actions(chess3.initial_state)
        self.assertEqual(2, len(actions3))
        actions4 = chess4.actions(chess4.initial_state)
        self.assertEqual(1, len(actions4))

        self.assertEqual(80 + 60 - 20, Chess.evaluation(chess1.initial_state.pieces, "S", configuration1.row_values))
        self.assertEqual(80 * 2 + 70 + 50 + 40 - 30, Chess.evaluation(chess2.initial_state.pieces, "S", configuration2.row_values))
        self.assertEqual(80 * 100 + 60 - 20, Chess.evaluation(chess3.initial_state.pieces, "S", configuration3.row_values))
        self.assertEqual(60 - 10 - 20, Chess.evaluation(chess4.initial_state.pieces, "S", configuration4.row_values))

        state = chess1.result(chess1.initial_state, actions1[0])
        self.assertEqual('C', state.to_move)
        self.assertEqual(len(chess1.initial_state.pieces), len(state.pieces))

        state = chess1.result(chess1.initial_state, actions1[1])
        self.assertEqual('C', state.to_move)
        self.assertEqual(len(chess1.initial_state.pieces), len(state.pieces) + 1)

        for a in actions2:
            state = chess2.result(chess2.initial_state, a)
            self.assertEqual('S', state.to_move)
            self.assertEqual(len(chess2.initial_state.pieces), len(state.pieces))

        state = chess3.result(chess3.initial_state, actions3[0])
        self.assertEqual('S', state.to_move)
        self.assertEqual(len(chess3.initial_state.pieces), len(state.pieces))

        state = chess3.result(chess3.initial_state, actions3[1])
        self.assertEqual('S', state.to_move)
        self.assertEqual(len(chess3.initial_state.pieces), len(state.pieces) + 1)

        for a in actions4:
            state = chess4.result(chess4.initial_state, a)
            self.assertEqual('C', state.to_move)
            self.assertEqual(len(chess4.initial_state.pieces), len(state.pieces))

        utility1 = minimax_decision(chess1.initial_state, chess1)
        self.assertEqual(80 * 2, utility1)
        chess2.initial_state.to_move = 'Circle'
        utility2 = minimax_decision(chess2.initial_state, chess2)
        self.assertEqual(-80 * 3 - 60 * 2, utility2)
        utility3 = minimax_decision(chess3.initial_state, chess3)
        self.assertEqual(80 - 80 * 100, utility3)
        # utility4 = minimax_decision(chess4.initial_state, chess4)
        # self.assertEqual(80 - 80 * 2, utility4)
