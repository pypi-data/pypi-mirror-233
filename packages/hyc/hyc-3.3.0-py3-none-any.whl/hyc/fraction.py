"""
This part named 'the fraction calculation', you can
use 'Fraction(denominator, numerator)' to make
a fraction and calculate it.

Thank you very much for using hyc library, I'll
make it even better for you!
"""

from typing import Union

from num import *


# 分数类
class Fraction:
    def __init__(self, numerator: int, denominator: int, num: int = 0):
        self.fraction = [numerator + num * denominator, denominator]

    # 分数化整数（保留到个位）
    def __int__(self):
        return self.fraction[1] // self.fraction[0] if self.fraction[1] > self.fraction[0] else 0

    # 读作
    def __repr__(self):
        return f'{self.fraction[0]}分之{self.fraction[1]}' if float(self) < 1 or float(
            self) % 1 == 0 else f'{self}又{self.fraction[0]}分之{self.fraction[1] % self.fraction[0]}'

    # 分数化小数
    def __float__(self):
        return self.fraction[1] / self.fraction[0]

    # 约分
    def fraction_reduction(self):
        if self.simple_fraction():
            return self
        else:
            common_div = gcd(self.fraction)[1]
            for i in range(2):
                self.fraction[i] = self.fraction[i] // common_div
            return self

    # 最简分数
    def simple_fraction(self):
        coprime(self.fraction)

    # 倒数
    def reciprocal(self):
        return Fraction(self.fraction[1], self.fraction[0])

    # 比较运算
    # x < y
    def __lt__(self, other):
        return float(self) < float(other)

    # x <= y
    def __le__(self, other):
        return float(self) <= float(other)

    # x == y
    def __eq__(self, other):
        return float(self) == float(other)

    # x != y
    def __ne__(self, other):
        return float(self) != float(other)

    # x > y
    def __gt__(self, other):
        return float(self) > float(other)

    # x >= y
    def __ge__(self, other):
        return float(self) >= float(other)

    # 分数运算（当分数为左操作数时）
    # 分数加整数（小数）
    def __add__(self, other):
        if type(other) == int or type(other) == float:
            other = convert(other)
        result = 0
        fraction_list = common_denominator([self, other])
        for i in fraction_list:
            result += i.fraction[1]
        fraction_sum = Fraction(fraction_list[0].fraction[0], result)
        return fraction_sum.fraction_reduction()

    # 分数减整数（小数）
    def __sub__(self, other):
        if type(other) == int or type(other) == float:
            other = convert(other)
        minuend, subtracted = common_denominator([self, other])
        minuend.fraction[1] -= subtracted.fraction[1]
        return minuend.fraction_reduction()

    # 分数乘整数（小数）
    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            other = convert(other)
        denominator = 1
        numerator = 1
        for i in [self.fraction, other.fraction]:
            denominator *= i[0]
            numerator *= i[1]
        result = Fraction(denominator, numerator)
        return result.fraction_reduction()

    # 分数除整数（小数）
    def __truediv__(self, other):
        if type(other) == int or type(other) == float:
            result = self * (1 / convert(other))
        return result.fraction_reduction()

    # 分数的整数次方
    def __pow__(self, power: int, modulo=None):
        return Fraction(self.fraction[0] ** power, self.fraction[1] ** power)

    # 分数整除整数（小数）
    def __floordiv__(self, other):
        return int(float(self) // float(other))

    # 分数运算（当分数为右操作数时）
    # 整数（小数）加分数
    def __radd__(self, other):
        return int(convert(other) + self)

    # 整数（小数）减分数
    def __rsub__(self, other):
        return int(convert(other) - self)

    # 整数（小数）乘分数
    def __rmul__(self, other):
        return int(convert(other) * self)

    # 整数（小数）除分数
    def __rtruediv__(self, other):
        return int(convert(other) / self)

    # 整数（小数）整除分数
    def __rfloordiv__(self, other):
        return int(float(other) // float(self))

    # 整数（小数）的分数次方
    def __rpow__(self, other):
        return other ** (1 / self.fraction[1]) ** self.fraction[0]


# 通分
def common_denominator(fraction_list: [Fraction, int]):
    fraction_list = [i.fraction_reduction() for i in fraction_list]
    denominators = [i.fraction[0] for i in fraction_list]
    for i in range(len(fraction_list)):
        factor = int(lcm(denominators) / denominators[i])
        fraction_list[i] = \
            Fraction(
                fraction_list[i].fraction[0] * factor,
                fraction_list[i].fraction[1] * factor
            )
    return fraction_list


# 整数（小数）化分数
def convert(num: Union[float, int]) -> Fraction:
    num = float(num)
    integer, decimal = str(num).split('.')
    result = Fraction(10 ** len(decimal), int(decimal), num=int(integer))
    return result.fraction_reduction()
