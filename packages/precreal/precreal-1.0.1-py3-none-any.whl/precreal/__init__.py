"""
precreal is a Python package, allowing you to compute floating point numbers without precision loss.

It is in pure Python and doesn't even use ctypes, so it is cross-platform and doesn't require a C/C++ library.

Works in Python 3, because in Python 3, integers are bignums, doesn't and never will work in Python 2.
"""
import sys as __sys

if hasattr(__sys, "set_int_max_str_digits"):
    __sys.set_int_max_str_digits(0)
from .precreal import *
from .algorithms import *
