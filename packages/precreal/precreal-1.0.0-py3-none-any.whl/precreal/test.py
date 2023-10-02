from . import *
from time import time


def _test():
    print("Test: phi computing (100 digits)")
    s = time()
    print(phi())
    print("{} seconds".format(time() - s))
    print("Test: phi computing (1000 digits)")
    s = time()
    print(phi(1000))
    print("{} seconds".format(time() - s))
    print("Test: pi computing (100 digits)")
    s = time()
    print(pi())
    print("{} seconds".format(time() - s))
    print("Test: pi computing (1000 digits)")
    s = time()
    print(pi(1000))
    print("{} seconds".format(time() - s))
    print("Test: Square root (100 digits)")
    s = time()
    print(sqrt(Real(2)))
    print("{} seconds".format(time() - s))
    print("Test: Square root (1000 digits)")
    s = time()
    print(sqrt(Real(2, precision=1000)))
    print("{} seconds".format(time() - s))


if __name__ == "__main__":
    _test()
