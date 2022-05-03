# PyFraction 클래스 테스트
# Python 3.10

from decimal import Decimal
from fractions import Fraction
import unittest

import pyfraction
from pyfraction import PyFraction


class PyFractionTest(unittest.TestCase):
    def test_is_fraction_form(self):
        testcases = ["1/2", "-1/3", "-10/011"]
        for testcase in testcases:
            self.assertTrue(pyfraction.is_fraction_form(testcase))
        testcases = ["A/2", "-1/0", "0", "0/0"]
        for testcase in testcases:
            self.assertFalse(pyfraction.is_fraction_form(testcase))

    def test_is_numeric_form(self):
        testcases = ["3", ".1", "0", "-1", "2.3", "-2.3"]
        for testcase in testcases:
            self.assertTrue(pyfraction.is_numeric_form(testcase))

    def test_constructor(self):
        with self.assertRaises(ZeroDivisionError):
            PyFraction(1, 0)
        testcases = (7, 9.123, Decimal("2.3"), "2.3", "4/5")
        for testcase in testcases:
            self.assertEqual(PyFraction(testcase).to_builtin(), Fraction(testcase))
        testcase = PyFraction(100, 101)
        self.assertEqual(PyFraction(testcase).to_builtin(), testcase.to_builtin())
        testcases = (
            PyFraction(1, 2),
            PyFraction(-1.2, 2.3),
            PyFraction(Decimal("3.7"), Decimal("4.7")),
            PyFraction("3.456", "7.898"),
            PyFraction("-3/457", "7/689"),
            PyFraction("-7.893", "3/123"),
        )
        for testcase in testcases:
            self.assertEqual(testcase.numerator, testcase.to_builtin().numerator)
            self.assertEqual(testcase.denominator, testcase.to_builtin().denominator)

    def test_repr(self):
        testcases = (PyFraction(-3, 8), PyFraction(3, 7), PyFraction("4.5"), PyFraction("7/9"))
        for testcase in testcases:
            self.assertEqual(eval(repr(testcase)), testcase)

    def test_operators1(self):
        self.assertEqual(-PyFraction(-2, 3), PyFraction(2, 3))
        self.assertEqual(+PyFraction(-2, 3), PyFraction(-2, 3))
        self.assertEqual(abs(PyFraction(-2, 3)), PyFraction(2, 3))
        self.assertEqual(abs(PyFraction(2, -3)), PyFraction(2, 3))
        self.assertEqual(float(PyFraction(-2, 3)), float(2 / -3))
        self.assertEqual(int(PyFraction(19, -3)), -19 // 3)
        self.assertEqual(hash(PyFraction(2, 3)), hash(PyFraction(4, 6)))

    def test_operators2(self):
        self.assertTrue(PyFraction(1 / 2) == PyFraction(1, 2) == PyFraction(2, 4))
        self.assertTrue(PyFraction(1 / 2) != PyFraction(1, 3))
        self.assertTrue(PyFraction(1 / 2) < PyFraction(2, 3))
        self.assertTrue(PyFraction(7, 10) > PyFraction(6 / 10))

    def test_operators3(self):
        self.assertEqual(PyFraction(1, 2) + PyFraction(1, 3), PyFraction(5, 6))
        self.assertEqual(PyFraction(1, 2) - PyFraction(1, 3), PyFraction(1, 6))
        self.assertEqual(PyFraction(1, 2) * PyFraction(1, 3), PyFraction(1, 6))
        self.assertEqual(PyFraction(1, 2) / PyFraction(1, 3), PyFraction(3, 2))
        self.assertEqual(PyFraction(2, 5) ** 3, PyFraction(2**3, 5**3))


if __name__ == "__main__":
    unittest.main()
