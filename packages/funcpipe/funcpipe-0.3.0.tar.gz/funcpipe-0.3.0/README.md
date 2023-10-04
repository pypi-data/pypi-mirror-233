Functional Utilities Library
This is a Python library that provides functional utilities for writing functional-style code in Python. The library includes the following utilities:

Pipe class
The Pipe class is a generic class that allows you to create a pipeline of functions that transform an input to an output. You can use the Pipe class to chain together multiple functions and apply them to an input value in a single expression. Here's an example:

```python
from functional_utils import Pipe

def add_one(x):
    return x + 1

def double(x):
    return x * 2

result = Pipe(add_one) >> double >> double >> add_one(3)
print(result)  # Output: 23
```

In this example, we create a Pipe object that applies the add_one function, then the double function twice, and finally the add_one function again to an input value of 3. The output of the pipeline is 23.

pattern_match function
The pattern_match function allows you to apply a transformer function based on the first predicate that matches the input value. You can use the pattern_match function to write code that selects a specific branch of execution based on the input value. Here's an example:

```python
from functional_utils import pattern_match

def is_even(x):
    return x % 2 == 0

def is_odd(x):
    return x % 2 == 1

def double(x):
    return x * 2

def triple(x):
    return x * 3

result = pattern_match(
    [
        (is_even, double),
        (is_odd, triple),
    ],
    default=lambda x: x,
)(5)

print(result)  # Output: 15
```

In this example, we create a Pipe object that applies the pattern_match function to an input value of 5. The pattern_match function selects the triple function because 5 is an odd number, and applies it to the input value. The output of the pipeline is 15.

Installation
You can install the library using pip:

```bash
pip install funcpipe
```

License
This library is licensed under the MIT License.

