# Higher-order Functions and Lambdas

OcellusScript supports writing functions that will accept functions as parameters. These functions, called higher-order functions, will usually take a function as one of its inputs or return a function as its output. OcellusScript comes with some higher-order functions for use with iteration and lists that are built into the [Hive module](./12-hive.md), the standard library module for OcellusScript.

## `for`

The `for` function takes three inputs: a starting value, and ending value, and a callable function to run. The callable function can be written by any means and supports the `where` expression. An example of the `for` function is provided with the `countToTen` example where a number is logged through each iteration.

```ocellusscript
import Hive only for

countToTen takes Nothing returns Nothing
countToTen = for 0 10 task where
                task i = log i
```

It important to note that the `for` function will automatically take care of increasing the start value and decreasing the end value.

More information on the `for` function can be found in the [Hive module documentation](./12-hive.md#for).

## `map`

The `map` function is a utility function that returns a list with a function applied to its elements. It accepts two parameters: the callable function to run on each element, and the list of items to run the callable function on. The following `mapIfTwo` function makes use of `map` to change a list of numbers into a list of booleans based on their divisibility:

```ocellusscript
import Hive only map

divisibleByTwo takes Integer returns Boolean
divisibleByTwo num = num % 2 == 0

mapIfTwo takes [Integer] returns [Boolean]
mapIfTwo list = map divisibleByTwo list
```

Note that the `divisibleByTwo` function does _not_ get called in the `mapIfTwo` definition as `map` will automatically handle this.

Below is the implementation for `map`:

More information on the `map` function can be found in the [Hive module documentation](./12-hive.md#map).

## `filter`

The `filter` function is a utility function that returns a list of items that obey a following condition. It accepts two parameters: the callable function that determines whether an item will be in the new list, and the list to filter. The following `containsBan` function makes use of `filter` to filter out any words in the list that do not contain the letters b, a, or n:

```ocellusscript
import Hive only filter, member

banHelper takes String returns Boolean
banHelper [] = true
banHelper x = member x "ban"
banHelper (x : xs) = (member x "ban") and (banHelper xs)

containsBan takes [String] returns [String]
containsBan list = filter banHelper list
```

Again, note that `banHelper` does _not_ get called in `containsBan` as `filter` handles this automatically.

More information on the `filter` function can be found in the [Hive module documentation](./12-hive.md#filter).

## `reduce`

The `reduce` function is a utility function that returns a single value of type `Anything` based on a method of reduction. It accepts three parameters: the callable function that dictates how values will be combined, the list to combine into a single value, and the starting value. The starting value will dictate what type the `reduce` function returns. The following `smartAdd` functions makes uses of `reduce` to add according to a specific set of rules:

```ocellusscript
import Hive only reduce

smartAdditionHelper takes Integer and Integer returns Integer
smartAdditionHelper x y = y % 3 == 0
                            ? x + (y * 4)
                            : x + y

smartAdd takes [Integer] returns Integer
smartAdd list = reduce smartAdditionHelper list 0
```

Again, note that `smartAdditionHelper` is _not_ called inside of the `smartAdd` function as `reduce` calls this automatically when running.

More information on the `reduce` function can be found in the [Hive module documentation](./12-hive.md#reduce).

## Lambda Functions

Sometimes it doesn't make sense to write a separate function to pass into a higher-order function like `map`. The `lambda` function is an in-line function that returns a function that evaluates a single expression from a select amount of parameters. The following example reduces the amount of code in `mapIfTwo` to use a lambda:

```ocellusscript
mapIfTwo takes [Integer] returns [Boolean]
mapIfTwo list = map (lambda x -> x % 2 == 0) list
```

This can also be used in cases like the `for` function:

```ocellusscript
countToFive takes Nothing returns Nothing
countToFive = for 0 5 (lambda x -> log x)
```