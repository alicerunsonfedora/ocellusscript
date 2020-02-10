# Defining Functions (Callables)

The bulk of OcellusScript's language works around defining functions, which evaluate expressions when called. For example, let's write a function that evaluates the square of a given integer. This can be done by writing the following:

```ocellusscript
square number = number * number
```

Where the following apply on the left side of the equal sign:

- `square` is the name of the function. To call this function at any time, we simply refer to `square`.
- `number` is the name of the argument that gets passed into the expression.

On the right side of the equal sign is the evaluation of the expression where we multiply the number we pass in by itself. Since the evaluation returns a number, the result of this evaluation will be the result of this function.

So, now, it's possible to call upon the `square` function and use its result elsewhere. For example:

```ocellusscript
square 4
```

Functions can also call upon other functions to make more complex results. For instance, the following function uses `square` in its evaluation:

```ocellusscript
evenSquare number = (square number) % 2 == 0
```

First, OcellusScript will evaluate the `square` function and then use its result to calculate whether or not dividing it by 2 will give a remainder.

OcellusScript will evaluate functions wrapped in parentheses (`()`) and work outward to the top level.

Functions can also have more than one parameter. For instance, if we wanted to write a function that determines whether or not two numbers are two away from each other, we can do the following:

```ocellusscript
offByTwo x y = y - x == 2
```

Where we now have two parameters, `x` and `y`. Order of parameters usually matters and will affect how the function is evaluated. Likewise, the `offByTwo` function can now be called as the following:

```ocellusscript
offByTwo 3 5
```

!!! warning "Function are Not Variables"
    It is important to keep in mind that writing functions in OcellusScript does not mean that they are variables. Any function definition is a Callable that usually returns a value. For instance, the following might look like a variable assignment in Python:

    ```
    helloWorld = "Hello, world!"
    ```

    When, in fact, this is _not_ a variable. This is a parameterless function that returns the evaluation of the string `"Hello, world!"`.


## Type Signatures

Type signatures are additional pieces of text above function definitions that help describe its parameters and its return type. This is used to describe the function and force type checking since OcellusScript doesn't require types to be declared immediately. For instance, let's refer to `helloWorld` again:

```ocellusscript
helloWorld takes Nothing returns String
helloWorld = "Hello, world!"
```

We can now clearly see that this function is indeed a function and that it has no parameters at all. Typically, type signatures will have the following pattern:

1. First, the function name is written to denote that the signature applies to that function. In this case, the function's name is `helloWorld`.
2. `takes` defines the parameters and its associated types. In this case, there are no parameters, so it takes a `Nothing` type.
3. `returns` defines the type that gets returned. In this case, the `String` type is returned.

Likewise, this can be applies to multi-parameter functions. Take a look at the type signature for `offByTwo`:

```ocellusscript
offByTwo takes Integer and Integer returns Boolean
offByTwo x y = y - x == 2
```

We can now see the following:

- `offByTwo` will only work with integers as their parameters. The `and` indicates the second parameter.
- `offByTwo` returns a boolean value instead of a number.

## Callables as Parameters in a Type Signature

There may be cases where a function itself is passed into another function as a parameter, like in [higher-order functions](../07-hoc/). To accomodate for this, the type signature can be modified to indicate that it takes a function (`Callable`) with its own parameters and return type. Take a look at the example below:

```ocellusscript
test takes (Callable takes Integer returns Integer) \
    and Integer returns Integer
```