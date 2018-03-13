from unittest import TestCase

from hw1cs561s2018 import Chess, Configuration, alphabeta_cutoff_search


class TestAlphabeta_search(TestCase):
    def test_action_no_action(self):
        configuration1 = Configuration(path=None)
        configuration1.generate_configuration_from_string(
            """Star
ALPHABETA
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
        chess1 = Chess(path=None, configuration=configuration1)
        utility1 = alphabeta_cutoff_search(chess1.initial_state, chess1, d=configuration1.depth_limit)
        self.assertEqual(((2, 3), (0, 1)), utility1[0])  # min action
        self.assertEqual(160, utility1[1])  # myopic
        self.assertEqual(160, utility1[2])  # farsighted
        self.assertEqual(4, utility1[3])  # total number

    def test_alphabeta_2(self):
        configuration1 = Configuration(path=None)
        configuration1.generate_configuration_from_string(
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
10,20,30,40,50,60,70,80""")
        chess1 = Chess(path=None, configuration=configuration1)
        utility1 = alphabeta_cutoff_search(chess1.initial_state, chess1, d=configuration1.depth_limit)
        self.assertEqual(('Noop'), utility1[0])  # min action
        self.assertEqual(-290, utility1[1])  # myopic
        self.assertEqual(-300, utility1[2])  # farsighted
        self.assertEqual(5, utility1[3])  # total number

    def test_alphabeta_3(self):
        configuration1 = Configuration(path=None)
        configuration1.generate_configuration_from_string(
            """Circle
ALPHABETA
10
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,C1,0,0,0
0,0,0,0,0,0,0,0
S1,0,S1,0,S1,0,S1,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
10,20,30,40,50,200,250,300
            """)
        chess1 = Chess(path=None, configuration=configuration1)
        utility1 = alphabeta_cutoff_search(chess1.initial_state, chess1, configuration1.depth_limit)
        print(chess1.translate(utility1))
        # self.assertEqual((('Noop')), utility1[0])
        # self.assertEqual(368, utility1[1])  # myopic
        # self.assertEqual(368, utility1[2])
        # self.assertEqual(3, utility1[3])
