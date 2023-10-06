import unittest
from parameterized import parameterized, parameterized_class
from xalgorithm.ods import (
    ArrayStack, ControlList, BaseList, ArrayQueue, ArrayDeque,
    power_analysis
)
from xalgorithm.utils import seed_all, random
from statsmodels.stats.power import tt_ind_solve_power

@parameterized_class( ('two_sided', 'kappa', 'expected'), [
    (True, 1, (4019,4019,8038)), (False, 1, (3166,3166,6332)),
    (True, 9, (20094,2233,22327)), (False, 9, (15828,1759,17587)),
])
class TestPowerAnalysis(unittest.TestCase):
    two_sided: bool; expected: tuple; kappa: int
    def setUp(self) -> None:
        self.mde = 0.5
        self.sigma = 8
        self.alpha = 0.05   # typei  = alpha = 5%
        self.power = 1-0.2  # typeii = beta  = 20%
    def test_power_analysis(self):
        n, na, nb = power_analysis(
            self.mde, self.alpha, self.power, self.sigma, 
            self.two_sided, self.kappa
        )
        nb_sm = tt_ind_solve_power(
            effect_size = self.mde / self.sigma,
            alpha=self.alpha, power = self.power, ratio=self.kappa, 
            alternative='two-sided' if self.two_sided else 'larger'
        )
        self.assertAlmostEqual(nb, nb_sm, delta=1)
        self.assertEqual(nb, self.expected[1])




class TestList(unittest.TestCase):
    l1: BaseList
    l2: BaseList
    n: int

def gen_list(ell=None, length=10):
    class MyListTest(unittest.TestCase):
        def setUp(self) -> None:
            self.l1 = ControlList() if ell is None else ell
            self.l2 = ControlList()
            self.n = length
            self._setUp()
        def tearDown(self) -> None:
            self.l1.clear()
            self.l2.clear()
        def _setUp(self):
            seed_all(5)
            for _ in range(length):
                x = random.random()
                i = random.randrange(0, len(self.l1)+1)
                self.l1.add(i, x)
                self.l2.add(i, x)
    return MyListTest

def test_list(self: TestList):
    l1, l2 = self.l1, self.l2 
    def get(add_one=False):
        i = random.randrange(0, len(l1) + add_one)
        x = random.random()
        return i, x
    for _ in range(5 * self.n):
        op = random.randrange(0,3)
        i, x = get(op==0)
        if op == 0:
            l1.add(i, x); l2.add(i, x)
        elif op == 1:
            l1.set(i, x); l2.set(i, x)
        else:
            l1.remove(i); l2.remove(i)
        self.assertListEqual(list(l1), list(l2))

NTest = 4

class TestArrayStack(gen_list(ArrayStack(), length=10)):
    @parameterized.expand(range(NTest))
    def test_array_stack(self, x):
        test_list(self) # type: ignore

class TestArrayQueue(unittest.TestCase):
    def test_array_queue(self):
        q = ArrayQueue()
        m, n = 10_000, 500
        for i in range(m):
            q.add(i)
            if q.size() > n:
                assert q.remove() == i - n

class TestArrayDeque(gen_list(ArrayDeque(), length=10)):
    @parameterized.expand(range(NTest))
    def test_array_deque(self, x):
        test_list(self) # type: ignore