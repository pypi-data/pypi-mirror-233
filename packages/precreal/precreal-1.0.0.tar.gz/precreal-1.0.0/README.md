This is a Python package to do exact real arithmetic, the following is an example using it:

```python
from precreal import Real,intpow

>>> 0.1+0.2==0.3 # Precision loss

False

>>> Real("0.1")+Real("0.2")==Real("0.3") # The Real class has NO precision loss when doing arithmetic

True

>>> intpow(Real(2),100)

1267650600228229401496703205376
```

You can also run `precreal_test`, which tests three features of this package.
