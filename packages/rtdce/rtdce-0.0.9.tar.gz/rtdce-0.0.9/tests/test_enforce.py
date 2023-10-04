from unittest import TestCase
from dataclasses import dataclass
from typing import List, Dict

from src.rtdce import enforce
from src.rtdce.exceptions import NotDataclassException


class TestEnforce(TestCase):
    def test_enforce_not_dataclass(self):
        class Test:
            pass

        t = Test()

        self.assertRaises(NotDataclassException, lambda: enforce(t))

    def test_enforce_dataclass(self):
        @dataclass
        class Test:
            test: str

        t = Test(test=1)
        self.assertRaises(TypeError, lambda: enforce(t))

    def test_enforce_complex_type(self):
        @dataclass
        class Test:
            test: List[str]
            test1: Dict[str, int]

        t = Test(test=["Hello"], test1={"test": 123})
        enforce(t)

    def test_enforce_complex_type_failing(self):
        @dataclass
        class Test:
            test: List[str]
            test1: Dict[str, int]

        t = Test(test=[True], test1={123: 0.123})
        self.assertRaises(TypeError, lambda: enforce(t))
