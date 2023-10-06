import unittest
from parameterized import parameterized_class
from xalgorithm.arrays import *
from xalgorithm import tag_me
from typing import List, TypeVar, Any

T = TypeVar('T')

@parameterized_class([ {"use_bfs": True}, {"use_bfs": False} ])
class TestHuaRongDao(unittest.TestCase):
    use_bfs: bool
    def test_hua_rong_dao(self):
        g = tag_me("Greedy")
        res = g.invoke("hua_rong_dao", [1, 2, 3, 0, 4], [0, 3, 2, 1, 4], self.use_bfs)
        self.assertEqual(res, 4)

@parameterized_class( ('n', 'input', 'expected_ntimes'), [
    (1, [20, 37, 20, 21, 37, 21, 21], [20, 37, 21]),
    (3, [1, 1, 3, 3, 7, 2, 2, 2, 2], [1,1,3,3,7,2,2,2]),
    (5, [], []),
    (0, [1, 2, 3, 1, 1, 2, 1, 2, 3, 3, 2, 4, 5, 3, 1], [])
])
class TestFreqLessThanNTimes(unittest.TestCase):
    input: List; n: int; expected_ntimes: List
    def test_freq_lt_ntimes(self):
        # 当某个数出现次数超过一定量的时候, 不再加入到返回列表中
        self.assertListEqual(freq_lt_ntimes(self.input, self.n), self.expected_ntimes)

@parameterized_class( ('input', 'flattened'), [
    ([2, 1, [3, [4, 5], 6], 7, [8]], [2, 1, 3, 4, 5, 6, 7, 8]),
    ([['d', ['e', 'f'], 'g'], 'h', ['i']], ['d', 'e', 'f', 'g', 'h', 'i']),
    ([[[]]], []),
])
class TestFlattenNestedArray(unittest.TestCase):
    input: List; flattened: List
    def test_flatten_nested_array(self):
        self.assertListEqual(flatten_nested_array(self.input), self.flattened) # type: ignore
        self.assertListEqual(list(flatten_nested_array(self.input, True)), self.flattened) 

@parameterized_class( ('skip', 'input', 'output'), [
    (3, list(range(1,10)), [3,6,9,4,8,5,2,7,1]),
    (2, list(range(1,10)), [2,4,6,8,1,5,9,7,3]),
    (3, list(range(1,5)), [3,2,4,1]),
])
class TestJosephusProblem(unittest.TestCase):
    skip: int; input: List; output: List
    def test_josephus_problem(self):
        res = josephus_problem(self.input, self.skip)
        self.assertListEqual(res, self.output)