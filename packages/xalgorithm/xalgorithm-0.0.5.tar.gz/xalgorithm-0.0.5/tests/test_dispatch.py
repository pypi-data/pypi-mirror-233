import unittest
from multipledispatch.dispatcher import Dispatcher
from multipledispatch import dispatch
from typing import Any, TypeVar

T = TypeVar("T")

def identity(x):
    return x

def inc(x):
    return x + 1

def dec(x):
    return x - 1

class A(object): pass
class B(object): pass
class C(A): pass
    
class TestDispatch(unittest.TestCase):
    def setUp(self) -> None:
        self.f = Dispatcher("f")
    def test_dispatcher(self):
        f = self.f
        f.add((int,), inc)
        f.add((float,), dec)
        self.assertEqual(f.dispatch(int), inc)
        self.assertEqual(f(1), 2)
        self.assertEqual(f(1.0), 0.0)
    def test_union(self):
        f = self.f
        f.register((int, float))(inc)
        self.assertEqual(f(1), 2)
        self.assertEqual(f(1.0), 2.0)
    def test_decorator(self):
        @dispatch((int, float))
        def inc(x): return x + 1
        self.assertEqual(inc(1), 2)
        self.assertEqual(inc(1.0), 2.0)
    def test_vararg(self):
        dispatch([object])
        def getN(*args): return len(args)
        self.assertEqual(getN('abc'), 1)
        self.assertEqual(getN(), 0)
    def test_inheritance(self):
        @dispatch(A)
        def getType(x): return A # type: ignore
        @dispatch(B)
        def getType(x): return B
        self.assertEqual(getType(C()), A)





