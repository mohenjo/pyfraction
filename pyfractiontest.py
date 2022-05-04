# PyFraction 클래스 테스트


import unittest
from decimal import Decimal
from fractions import Fraction

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
        self.assertEqual(PyFraction(2, 5) ** 3, PyFraction(2 ** 3, 5 ** 3))

    def test_property(self):
        self.assertEqual(PyFraction(1, 2).numerator, 1)
        self.assertEqual(PyFraction(1, 2).denominator, 2)
        self.assertEqual(PyFraction(1, -2).members, (-1, 2))

    def test_to_builtin(self):
        self.assertEqual(PyFraction(1, 2).to_builtin(), Fraction(1, 2))
        self.assertEqual(PyFraction(1, -2).to_builtin(), Fraction(-1, 2))

    def test_to_decimal(self):
        self.assertEqual(PyFraction(1, 2).to_decimal(), Decimal("0.5"))
        self.assertEqual(PyFraction(1, -2).to_decimal(), Decimal("-0.5"))

    def test_get_reciprocal(self):
        self.assertEqual(PyFraction(1, 2).get_reciprocal(), PyFraction(2, 1))
        self.assertEqual(PyFraction(1, -2).get_reciprocal(), PyFraction(-2, 1))

    def test_is_proper(self):
        self.assertTrue(PyFraction(1, 2).is_proper())
        self.assertFalse(PyFraction(5, 3).is_proper())

    def test_is_improper(self):
        self.assertFalse(PyFraction(1, 2).is_improper())
        self.assertTrue(PyFraction(5, 3).is_improper())

    def test_is_integer(self):
        self.assertTrue(PyFraction(7, 7).is_integer())
        self.assertFalse(PyFraction(7, 6).is_integer())

    def test_get_whole_number(self):
        self.assertEqual(PyFraction(7, 7).get_whole_number(), 1)
        self.assertEqual(PyFraction(7, 6).get_whole_number(), 1)
        self.assertEqual(PyFraction(5, 6).get_whole_number(), 0)
        self.assertEqual(PyFraction(6, 3).get_whole_number(), 2)

    def test_limit_denominator(self):
        self.assertEqual(PyFraction('3.1415926535897932').limit_denominator(1000), PyFraction(355, 113))
        self.assertEqual(PyFraction(1.1).limit_denominator(), PyFraction(11, 10))
        self.assertEqual(PyFraction(0.333333).limit_denominator(1000), PyFraction(1, 3))
        self.assertEqual(PyFraction(0.166666).limit_denominator(1000), PyFraction(1, 6))
        self.assertEqual(PyFraction(0.142857142857142857).limit_denominator(1000), PyFraction(1, 7))

    def test_get_egyptian_expression(self):
        target_val: set[PyFraction] = {PyFraction(1, 3), PyFraction(1, 15)}
        self.assertEqual(set(PyFraction(2, 5).get_egyptian_expression()), target_val)
        target_val: set[PyFraction] = {PyFraction(1, 2), PyFraction(1, 8)}
        self.assertEqual(set(PyFraction(5, 8).get_egyptian_expression()), target_val)

    def test_from_str(self):
        self.assertEqual(PyFraction.from_str('1/2'), PyFraction(1, 2))
        self.assertEqual(PyFraction.from_str('-2/3'), PyFraction(-2, 3))

    def test_from_number(self):
        self.assertEqual(PyFraction.from_number(1.5), PyFraction(3, 2))
        self.assertEqual(PyFraction.from_number(-3), PyFraction(3, -1))
        self.assertEqual(PyFraction.from_number(Decimal("2.5")), PyFraction(5, 2))

    def test_from_builtin(self):
        self.assertEqual(PyFraction.from_builtin(Fraction(1, 2)), PyFraction(1, 2))
        self.assertEqual(PyFraction.from_builtin(Fraction(-2, 3)), PyFraction(-2, 3))

    def test_from_other(self):
        self.assertEqual(PyFraction.from_other(PyFraction(1, 2)), PyFraction(1, 2))


if __name__ == "__main__":
    unittest.main()
