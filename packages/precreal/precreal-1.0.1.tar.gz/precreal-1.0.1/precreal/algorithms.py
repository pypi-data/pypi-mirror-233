"""
Some algorithms for the Real type in precreal
"""
from .precreal import Real
from copy import deepcopy


def intpow(x, y):
    """
    Computes x**y
    :param x: Real
    :param y: integer
    :return: Real
    """
    a = deepcopy(x, {})
    result = Real(1, precision=x.precision, simplify=x.simplify)
    while y:
        if y % 2:
            result *= a
        y //= 2
        a *= a
    return result


def root(x, y):
    """
    Computes x**(1/y) (up to x.precision)
    :param x: Real
    :param y: integer
    :return: x**(1/y)
    """
    if y % 2 == 0 and x.sign() == -1:
        raise ValueError("Result not a real number")
    z = Real(1, 10**x.precision, precision=x.precision, simplify=x.simplify)
    l, r = Real(0, precision=x.precision, simplify=x.simplify), max(
        x, Real(1, precision=x.precision, simplify=x.simplify)
    )
    while abs(l - r) >= z:
        mid = (l + r) / 2
        if intpow(mid, y) > x:
            r = mid
        else:
            l = mid
    return l


def pow(x, y):
    """
    Computes x**y (up to x.precision), if the exponent is an integer, it is recommended to use intpow() instead
    >>> pow(Real(2),Real(1,2))
    1.4142135623730950488016887242096980785696718753769480731766797379907324784621070388503875343276415727
    >>> pow(Real(2),Real(3))
    8
    :param x: Real
    :param y: Real
    :return: Real
    """
    if not isinstance(y, Real):
        y = Real(y)
    if not isinstance(x, Real):
        x = Real(x)
    result = root(intpow(x, y.numerator), y.denominator)
    if y.sign == -1:
        result = Real(
            result.denominator,
            result.numerator,
            simplify=result.simplify,
            precision=result.precision,
        )
    return result


sqrt = lambda x: root(x, 2)


def phi(prec=100):
    """
    Computes phi
    >>> phi()
    1.6180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911374
    >>> phi(2)
    1.61
    :param prec: digits
    :return: a Real object with precision prec, represents phi
    """
    return (Real(1, precision=prec) + sqrt(Real(5, precision=prec))) / Real(
        2, precision=prec
    )


def pi(prec=100):
    """
    Computes pi
    >>> pi()
    3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651
    >>> pi(2)
    3.14
    :param prec: digits
    :return: a Real object with precision prec, represents pi
    """
    prec += 10
    r = Real(0, precision=prec)
    for i in range(prec):
        r += intpow(Real(1, 5, precision=prec), i * 4 + 1) / (i * 4 + 1) - intpow(
            Real(1, 5, precision=prec), i * 4 + 3
        ) / (i * 4 + 3)
    s = Real(0, precision=prec)
    for i in range(prec):
        s += intpow(Real(1, 239, precision=prec), i * 4 + 1) / (i * 4 + 1) - intpow(
            Real(1, 239, precision=prec), i * 4 + 3
        ) / (i * 4 + 3)
    a = r * 16 - s * 4
    a.precision = prec
    return a


def rand(prec=100, use_secrets=True):
    """
    Return a random Real number in [0,1)
    >>> rand()
    0.6430997410264154172521480037843260492523013140407526344628086475835143370634611004596928411125970842
    >>> rand(2)
    0.41
    :param prec: digits
    :param use_secrets: Whether to use the "secrets" module in Python if available, if this is set to False or if the "secrets" module is unavailable, it uses the "random" module
    :return: a random number
    """
    if use_secrets:
        try:
            import secrets

            return Real(secrets.randbelow(10**prec), 10**prec, precision=prec)
        except:
            from random import randint

            return Real(randint(0, 10**prec - 1), 10**prec, precision=prec)
    else:
        from random import randint

        return Real(randint(0, 10**prec - 1), 10**prec, precision=prec)


__all__ = ["pow", "sqrt", "phi", "pi", "rand", "intpow"]
