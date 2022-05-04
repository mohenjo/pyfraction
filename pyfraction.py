"""PyFraction

파이썬 내장 `fractions.Fraction` 클래스의 재구현 및 확장

Version: 1.0.2022.0504

Author: Haennim Park
"""

import fractions
import math
import numbers
import re
from decimal import Decimal
from typing import Union


# region Globals

def is_fraction_form(form: str):
    """입력 인자가 분수 형태인지 확인합니다."""
    pattern = re.compile(r"^-?\d+/-?0*[1-9]\d*$")
    return pattern.search(form) is not None


def is_numeric_form(form: str):
    """입력 인자가 숫자 형태인지 확인합니다."""
    try:
        float(form)
        return True
    except ValueError:
        return False


# endregion

# region PyFraction
class PyFraction:
    """분수 클래스

    이 클래스는 파이썬 built-in fractions.Fraction 클래스를 재구현 및 확장한 것입니다.
    """

    def __init__(self, numerator: object, denominator: object = None) -> None:
        """이 클래스의 인스턴스를 생성합니다.

        Args:
            numerator (object): 분자. 지원타입: int, float, decimal.Decimal, numbers.Rational, str, PyFraction
            denominator (object, optional): 분모. None이 아닐 경우 분자와 호환되는 타입입니다. 기본값은 None.

        Raises:
            TypeError: 변환 가능한 타입 또는 형식이 아닐 경우
            ZeroDivisionError: 분모가 영(0)으로 주어진 경우
        """
        # 분모가 주어지지 않은 경우
        if denominator is None:
            if isinstance(numerator, (int, float, Decimal)):
                self.__numerator, self.__denominator = numerator.as_integer_ratio()
            elif isinstance(numerator, numbers.Rational):
                self.__numerator = numerator.numerator
                self.__denominator = numerator.denominator
            elif isinstance(numerator, str):
                if is_fraction_form(numerator):
                    (self.__numerator, self.__denominator) = (int(s) for s in numerator.split("/"))
                elif is_numeric_form(numerator):
                    self.__numerator, self.__denominator = Decimal(numerator).as_integer_ratio()
                else:
                    raise TypeError(f"'{numerator}'는 분수 형태로 변환할 수 없습니다.")
            elif isinstance(numerator, PyFraction):
                self.__numerator = numerator.numerator
                self.__denominator = numerator.denominator
            else:
                raise TypeError(f"{numerator}는 분수 형태로 변환할 수 없습니다.")
        # 분모가 None이 아닌 경우 - numerator와 denominator는 호환되는 타입이어야 합니다.
        elif isinstance(numerator, (int, float, Decimal)) and isinstance(denominator, (int, float, Decimal)):
            num_num, num_den = numerator.as_integer_ratio()
            den_num, den_den = denominator.as_integer_ratio()
            self.__numerator = num_num * den_den
            self.__denominator = num_den * den_num
        elif isinstance(numerator, numbers.Rational) and isinstance(denominator, numbers.Rational):
            self.__numerator = numerator.numerator * denominator.denominator
            self.__denominator = numerator.denominator * denominator.numerator
        elif isinstance(numerator, str) and isinstance(denominator, str):
            if not (
                    is_fraction_form(numerator)
                    or is_fraction_form(denominator)
                    or is_numeric_form(numerator)
                    or is_numeric_form(denominator)
            ):
                raise TypeError(f"'{numerator}` 또는 `{denominator}'를 분수 형태로 변환할 수 없습니다.")
            if is_fraction_form(numerator):
                num_num, num_den = (int(s) for s in numerator.split("/"))
            else:  # is_numeric_form(numerator):
                num_num, num_den = float(numerator).as_integer_ratio()
            if is_fraction_form(denominator):
                den_num, den_den = (int(s) for s in denominator.split("/"))
            else:  # is_numeric_form(denominator):
                den_num, den_den = float(denominator).as_integer_ratio()
            self.__numerator = num_num * den_den
            self.__denominator = num_den * den_num
        elif isinstance(numerator, PyFraction) and isinstance(denominator, PyFraction):
            self.__numerator = numerator.numerator * denominator.denominator
            self.__denominator = numerator.denominator * denominator.numerator
        else:
            raise TypeError(f"{numerator}/{denominator}는 분수 형태로 변환할 수 없습니다.")

        if self.__denominator == 0:
            raise ZeroDivisionError("분모는 영(0)이 될 수 없습니다.")

        # Normalize:
        # 1. 분수 클래스의 부호는 항상 분자에 적용
        # 2. 기약 분수의 형태로 변환
        self.__sign: int = int(math.copysign(1, self.__numerator) * math.copysign(1, self.__denominator))
        gcd: int = math.gcd(abs(self.__numerator), abs(self.__denominator))
        self.__numerator: int = self.__sign * (abs(self.__numerator) // gcd)
        self.__denominator: int = abs(self.__denominator) // gcd
        self.__members: tuple[int, int] = (self.__numerator, self.__denominator)

    def __str__(self) -> str:
        return f"{self.numerator}/{self.denominator}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.numerator}, {self.denominator})"

    def __neg__(self) -> "PyFraction":
        return PyFraction(-self.numerator, self.denominator)

    def __pos__(self) -> "PyFraction":
        return self

    def __abs__(self) -> "PyFraction":
        return PyFraction(abs(self.numerator), abs(self.denominator))

    def __float__(self) -> float:
        return float(self.numerator / self.denominator)

    def __int__(self) -> int:
        return int(self.numerator // self.denominator)

    def __hash__(self) -> int:
        return hash(self.__members)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PyFraction):
            return self.members == other.members
        return False

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __lt__(self, other: "PyFraction") -> bool:
        return self.to_decimal() < other.to_decimal()

    def __le__(self, other: "PyFraction") -> bool:
        return self.to_decimal() <= other.to_decimal()

    def __gt__(self, other: "PyFraction") -> bool:
        return self.to_decimal() > other.to_decimal()

    def __ge__(self, other: "PyFraction") -> bool:
        return self.to_decimal() >= other.to_decimal()

    # Augmented Assignment(+=, -=, *=, /=, ...) 구현을 위해
    # __iadd__, __isub__, ... 등의 연산자 오버로딩을 별도로 구현하지 않습니다.
    # 상기의 매직 메소드는 연산의 결과로 (새로운 객체를 반환하는 것이 아니라) 기존 객체를 변경하는 것이며,
    # 따라서, 본 클래스 구현에 의한 Augmented Assignment는 새로운 객체를 반환하게 됩니다.
    # 참고: https://stackoverflow.com/questions/1047021/overriding-in-python-iadd-method

    def __add__(self, other: "PyFraction") -> "PyFraction":
        lcm: int = math.lcm(self.denominator, other.denominator)
        new_numerator = (lcm // self.denominator) * self.numerator + (lcm // other.denominator) * other.numerator
        return PyFraction(new_numerator, lcm)

    def __sub__(self, other: "PyFraction") -> "PyFraction":
        return self.__add__(-other)

    def __mul__(self, other: "PyFraction") -> "PyFraction":
        return PyFraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other: "PyFraction") -> "PyFraction":
        return self * other.get_reciprocal()

    def __pow__(self, power: int) -> "PyFraction":
        return PyFraction(self.numerator ** power, self.denominator ** power)

    @property
    def numerator(self) -> int:
        """분모"""
        return self.__numerator

    @property
    def denominator(self) -> int:
        """분자"""
        return self.__denominator

    @property
    def members(self) -> tuple[int, int]:
        """(분자:int, 분모:int) 형태의 tuple 객체를 반환합니다."""
        return self.__members

    def to_builtin(self) -> fractions.Fraction:
        """이 클래스의 인스턴스에 해당하는 fraction.Fraction 객체를 반환합니다."""
        return fractions.Fraction(self.numerator, self.denominator)

    def to_decimal(self) -> Decimal:
        """decimal.Decimal 값으로 변환합니다."""
        return Decimal(self.numerator) / Decimal(self.denominator)

    def get_reciprocal(self) -> "PyFraction":
        """역수를 반환합니다."""
        return PyFraction(self.denominator, self.numerator)

    def is_proper(self) -> bool:
        """진분수(proper fraction)인지 확인합니다."""
        return self.numerator < self.denominator

    def is_improper(self) -> bool:
        """가분수(improper fraction)인지 확인합니다."""
        return self.numerator > self.denominator

    def is_integer(self) -> bool:
        """분수의 값이 정수인지 확인합니다."""
        return self.numerator % self.denominator == 0

    def get_whole_number(self) -> int:
        """(가)분수의 정수부를 반환합니다."""
        return self.numerator // self.denominator

    def limit_denominator(self, max_denominator: int = 1_000_000):
        """분모가 최대 max_denominator인 현재 인스턴스에 가장 가까운 인스턴스를 반환합니다. 이 메서드는 특히 순환 소수를 변환하는데 유용합니다:"""
        if max_denominator < 1:
            raise ValueError("max_denominator must be greater than 0")
        if self.denominator <= max_denominator:
            return PyFraction(self)

        p0, q0, p1, q1 = 0, 1, 1, 0
        n, d = self.numerator, self.denominator
        while True:
            a = n // d
            q2 = q0 + a * q1
            if q2 > max_denominator:
                break
            p0, q0, p1, q1 = p1, q1, p0 + a * p1, q2
            n, d = d, n - a * d

        k = (max_denominator - q0) // q1
        bound1 = PyFraction(p0 + k * p1, q0 + k * q1)
        bound2 = PyFraction(p1, q1)
        if abs(bound2 - self) <= abs(bound1 - self):
            return bound2
        return bound1

    def get_egyptian_expression(self) -> list["PyFraction"]:
        """이집트식 분수 표기법(단위 분수의 합)으로 변환합니다."""
        pyfractions: list[PyFraction] = []
        target_fraction: PyFraction = self
        last_denominator: int = 2
        while True:
            check_fraction: PyFraction = PyFraction(1, last_denominator)
            while check_fraction >= target_fraction:
                last_denominator += 1
                check_fraction = PyFraction(1, check_fraction.denominator + 1)
            pyfractions.append(check_fraction)
            target_fraction = PyFraction(target_fraction - check_fraction)
            last_denominator += 1
            if target_fraction.numerator == 1:
                break

        pyfractions.append(target_fraction)
        return pyfractions

    @classmethod
    def from_str(cls, num_str: str) -> "PyFraction":
        """str 객체로부터 이 클래스의 인스턴스를 생성합니다."""
        return cls(num_str)

    @classmethod
    def from_number(cls, number: Union[int, float, Decimal, numbers.Rational]) -> "PyFraction":
        """int, float, decimal.Decimal, numbers.Rational 값으로부터 이 클래스의 인스턴스를 생성합니다."""
        return cls(number)

    @classmethod
    def from_builtin(cls, fraction: fractions.Fraction) -> "PyFraction":
        """fraction.Fraction 객체로부터 이 클래스의 인스턴스를 생성합니다."""
        return cls(fraction.numerator, fraction.denominator)

    @classmethod
    def from_other(cls, fraction: "PyFraction") -> "PyFraction":
        """이 클래스의 인스턴스로부터 이 클래스의 인스턴스를 생성합니다."""
        return cls(fraction.numerator, fraction.denominator)

# endregion
