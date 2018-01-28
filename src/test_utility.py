from unittest import TestCase

from hw1cs561s2018 import Configuration


class TestUtility(TestCase):
    configuration = Configuration(path=None)
    configuration.player = "S"
    configuration.row_values = [10, 20, 30, 40, 50, 60, 70, 80]
