"""
Provides the Real object for exact arithmetic
"""
from math import gcd
from functools import wraps


def simplifier(func):
    @wraps(func)
    def infunc(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)
        if not self.simplify:
            return ret
        g = gcd(self.numerator, self.denominator)
        self.numerator //= g
        self.denominator //= g
        return ret

    return infunc


class Real:
    precision = 100  # Default precision
    simplify = True  # To or not to simplify the fraction after an operation (Note: without simplification it will be much faster)

    def __init__(self, *args, simplify=True, precision=100):
        """
        Provides a lossless real number
        Real(value)
        Converts the given value into Real object, supports integer, string, another Real and float
        For example:
        >>> Real(1)
        1
        >>> Real("2")
        2
        >>> Real(0.5)
        0.5
        >>> Real(0.1)
        0.1000000000000000055511151231257827021181583404541015625
        Real(numerator,denominator)
        Converts the fraction numerator/denominator into Real object, it is exact.
        >>> Real(1,10)
        0.1
        >>> Real(Real(1))
        1

        the precision and simplify arguments controls precision and simplification
        """
        self.precision = precision
        self.simplify = simplify
        if len(args) == 2:
            self.numerator, self.denominator = args
        elif len(args) == 1:
            if isinstance(args[0], int):
                self.numerator, self.denominator = args[0], 1
            elif isinstance(args[0], str):
                pos = args[0].find(".")
                if pos == -1:
                    self.numerator, self.denominator = int(args[0]), 1
                else:
                    self.numerator, self.denominator = int(
                        args[0].replace(".", "")
                    ), 10 ** len(args[0][pos + 1 :])
            elif isinstance(args[0], float):
                s = "%.100f" % args[0]
                pos = s.find(".")
                if pos == -1:
                    self.numerator, self.denominator = int(s), 1
                else:
                    a, b = s.split(".")
                    self.numerator, self.denominator = int(
                        a + b.rstrip("0")
                    ), 10 ** len(b.rstrip("0"))
            elif isinstance(
                args[0], Real
            ):  # In this case, the precision argument and simplify arguments are ignored
                self.precision = args[0].precision
                self.numerator = args[0].numerator
                self.denominator = args[0].denominator
                self.simplify = args[0].simplify
            else:
                raise TypeError("Only supports int, str, Real and float")
        else:
            raise ValueError("Real class only accepts one or two positional arguments")
        if self.simplify:
            g = gcd(self.numerator, self.denominator)
            self.numerator //= g
            self.denominator //= g

    @simplifier
    def tofraction(self):
        """
        Convert self to a fraction string
        >>> a=Real(0.1)
        >>> a.tofraction()
        '3602879701896397/36028797018963968'
        >>> b=Real(0.1,simplify=False)
        >>> b.tofraction() # If you don't want the number to be simplified, the fraction remains unsimplified, too.
        1000000000000000055511151231257827021181583404541015625/10000000000000000000000000000000000000000000000000000000
        :return: The fraction as a string, "a/b" if it is not an integer, or "a" if it is an integer
        """
        if self.denominator == 1:
            return str(self.numerator)
        if self.denominator == -1:
            return "-" + str(self.numerator)
        return str(abs(self.numerator) * self.sign()) + "/" + str(abs(self.denominator))

    @simplifier
    def tostring(self):
        """
        Convert self to a decimal string, this operation removes the trailing zeros
        >>> a=Real(0.1) # Python's built-in float is inaccurate
        >>> a.tostring()
        '0.1000000000000000055511151231257827021181583404541015625'
        >>> a.precision=10
        >>> a.tostring()
        '0.1'
        >>> b=Real("0.1") # Exact
        >>> b.tostring()
        '0.1'
        >>> c=Real(1)/Real(7)
        >>> c.tostring()
        '0.1428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428'
        >>> c.precision=10
        >>> c.tostring() # Truncated output string
        '0.1428571428'
        >>> c.precision=100
        >>> c.tostring() # Precision does not lose after truncation
        '0.1428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428'
        :return: The decimal string
        """
        self.numerator *= self.sign()
        self.denominator = abs(self.denominator)
        intpart, floatpart = (
            self.sign() * (abs(self.numerator) // self.denominator),
            abs(self.numerator) % self.denominator,
        )
        result = str(intpart)
        result_floatpart = ""
        if self.precision <= 0:
            return result
        for i in range(self.precision):  # Multiply 10 repeatedly
            floatpart *= 10
            result_floatpart += str(floatpart // self.denominator)
            floatpart %= self.denominator
        result_floatpart = result_floatpart.rstrip("0")
        if not result_floatpart:
            return result
        return result + "." + result_floatpart

    def __truediv__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        return Real(
            self.numerator * b.denominator,
            self.denominator * b.numerator,
            simplify=self.simplify or b.simplify,
            precision=max(self.precision, b.precision),
        )

    def __floordiv__(self, b):  # Warning: This returns a regular Python integer
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        return (self.numerator * b.denominator) // (self.denominator * b.numerator)

    def __trunc__(self):
        return self.numerator // self.denominator

    def __float__(self):
        return self.numerator / self.denominator

    def sign(self):
        """
        Get the sign of self
        :return: -1 if self is negative, 0 if self is zero, and 1 if self is positive
        """
        if self.numerator * self.denominator == 0:
            return 0
        return (
            self.numerator * self.denominator // abs(self.numerator * self.denominator)
        )

    def __mul__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        return Real(
            self.numerator * b.numerator,
            self.denominator * b.denominator,
            simplify=self.simplify or b.simplify,
            precision=max(self.precision, b.precision),
        )

    def __add__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        return Real(
            self.numerator * b.denominator + self.denominator * b.numerator,
            self.denominator * b.denominator,
            simplify=self.simplify or b.simplify,
            precision=max(self.precision, b.precision),
        )

    def __sub__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        return Real(
            self.numerator * b.denominator - self.denominator * b.numerator,
            self.denominator * b.denominator,
            simplify=self.simplify or b.simplify,
            precision=max(self.precision, b.precision),
        )

    def __neg__(self):
        return Real(
            -self.numerator,
            self.denominator,
            simplify=self.simplify,
            precision=self.precision,
        )

    def __abs__(self):
        return Real(
            abs(self.numerator),
            abs(self.denominator),
            simplify=self.simplify,
            precision=self.precision,
        )

    def __gt__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        return self.numerator * b.denominator > self.denominator * b.numerator

    def __eq__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        return self.numerator * b.denominator == self.denominator * b.numerator

    def __ne__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        return self.numerator * b.denominator != self.denominator * b.numerator

    def __lt__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        return self.numerator * b.denominator < self.denominator * b.numerator

    def __ge__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        return self.numerator * b.denominator >= self.denominator * b.numerator

    def __le__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        return self.numerator * b.denominator <= self.denominator * b.numerator

    def __iadd__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        x = self.__add__(b)
        self.numerator, self.denominator = x.numerator, x.denominator
        return self

    def __isub__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        x = self.__sub__(b)
        self.numerator, self.denominator = x.numerator, x.denominator
        return self

    def __imul__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        x = self.__mul__(b)
        self.numerator, self.denominator = x.numerator, x.denominator
        return self

    def __itruediv__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        x = self.__truediv__(b)
        self.numerator, self.denominator = x.numerator, x.denominator
        return self

    def __ifloordiv__(
        self, b
    ):  # Warning: This results in a Real object with the same value as the corresponding integer
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        self.numerator, self.denominator = self.__floordiv__(b), 1
        return self

    def __deepcopy__(self, *_, **__):
        return Real(
            self.numerator,
            self.denominator,
            precision=self.precision,
            simplify=self.simplify,
        )

    def __hash__(self):
        return hash((self.numerator, self.denominator))

    def __pow__(self, b, *_, **__):
        from .algorithms import pow

        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        return pow(self, b)

    def __ipow__(self, b, *_, **__):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        x = self.__pow__(b)
        self.numerator, self.denominator = x.numerator, x.denominator
        return self

    def __mod__(self, b):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        if not b:  # Any number % 0 is 0
            return Real(0, simplify=self.simplify, precision=self.precision)
        return Real(
            (self.numerator * b.denominator) % (self.denominator * b.numerator),
            self.denominator * b.numerator,
            simplify=self.simplify,
            precision=self.precision,
        )

    def __imod__(self, b, *_, **__):
        if not isinstance(b, Real):
            b = Real(b, simplify=self.simplify, precision=self.precision)
        x = self.__mod__(b)
        self.numerator, self.denominator = x.numerator, x.denominator
        return self

    __int__ = __trunc__
    __bool__ = lambda _: _.numerator != 0
    __repr__ = lambda *_: _[0].tostring(*_[1:])
    __str__ = lambda *_: _[0].tostring(*_[1:])


__all__ = ["Real"]
