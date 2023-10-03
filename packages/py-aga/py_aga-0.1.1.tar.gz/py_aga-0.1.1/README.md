Aga is a lightweight native Python library for quickly creating documented command-line interfaces using `argparse`. It is designed to be as simple as possible to use.

## Usage
Using Aga couldn't be easier. Assume the file below is named _test.py_: 

```
from aga import *


@aga.add_arg
def add(first: int, second: int = 2) -> int:
    """ A simple function to add two numbers

    Args:
        first: One of the numbers to add
        second: The other number to add

    Returns:
        first added to second
    """

    return x + y


if __name__ == '__main__':
    aga.bake()
    print(aga.args.first, aga.args.second)

```

This simple file will result in the `x` and `y` arguments as shown below in the output of `python test.py -h`.

```
❯ python test.py -h
usage: test.py [-h] [-s] [-f]

options:
  -h, --help      show this help message and exit
  -s , --second   The other number to add
  -f , --first    One of the numbers to add
```

As you can see, one must simply add the decorator `aga.add_arg` to a function and Aga will parse the function definition and create a documented command-line interface. 

Aga will search for PEP484 type annotations, default values and Google-style docstrings to add further information to the argument definition. None of these are necessary however, and if one (or all) are missing it will simply be ignored.