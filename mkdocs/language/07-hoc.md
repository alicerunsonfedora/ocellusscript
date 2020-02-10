# Higher-order Functions and Lambda Expressions

OcellusScript supports writing functions that will accept functions as parameters. These functions, called higher-order functions, will usually take a function as one of its inputs or return a function as its output. OcellusScript comes with some built-in higher-order functions for use with iteration and lists.

## `for`

The `for` function takes three inputs: a starting value, and ending value, and a callable function to run. The callable function can be written by any means and supports the `where` expression. An example of the `for` function is provided with the `countToTen` example where a number is logged through each iteration.

```ocellusscript
countToTen takes Nothing returns Nothing
countToTen = for 0 10 task where
                task i = log i
```

It important to note that the `for` function will automatically take care of increasing the start value and decreasing the end value.

The following is an implementation of the `for` function:
```ocellusscript
for takes Integer and Integer and \
    (Callable takes Anything? returns Anything?) returns Nothing
for start end task = forHelper start start end task where
                        forHelper i n j t = j == n
                                            ? t
                                            : forHelper (i + 1) n (j - 1) t
```

## `map`

The `map` function is a utility function that returns a list with a function applied to its elements. It accepts two parameters: the callable function to run on each element, and the list of items to run the callable function on. The following `mapIfTwo` function makes use of `map` to change a list of numbers into a list of booleans based on their divisibility:

```ocellusscript
divisibleByTwo takes Integer returns Boolean
divisibleByTwo num = num % 2 == 0

mapIfTwo takes [Integer] returns [Boolean]
mapIfTwo list = map divisibleByTwo list
```

Note that the `divisibleByTwo` function does _not_ get called in the `mapIfTwo` definition as `map` will automatically handle this.

Below is the implementation for `map`:

```ocellusscript
map takes (Callable takes Anything returns Anything) and [Anything] \
    returns [Anything]
map func x = helper func x [] where
                helper func [] list = list
                helper func i list = list + [func i]
                helper func (i:j) list = helper func j (list + [func i])
```

## `filter`

The `filter` function is a utility function that returns a list of items that obey a following condition. It accepts two parameters: the callable function that determines whether an item will be in the new list, and the list to filter. The following `containsBan` function makes use of `filter` to filter out any words in the list that do not contain the letters b, a, or n:

```ocellusscript
banHelper takes String returns Boolean
banHelper [] = true
banHelper x = member x "ban"
banHelper (x : xs) = (member x "ban") and (banHelper xs)

containsBan takes [String] returns [String]
containsBan list = filter banHelper list
```

Again, note that `banHelper` does _not_ get called in `containsBan` as `filter` handles this automatically.

Below is the implementation for `filter`:
```ocellusscript
filter takes (Callable takes Anything returns Boolean) and [Anything] \
    returns [Anything]
filter f x = helper f x [] where
                helper func [] list = list
                helper func i list = (func i) 
                                            ? list + [i] 
                                            : list
                helper func (i:j) list = helper func j (func i)
                                                        ? list + [i] 
                                                        : list)
```

## `reduce`

The `reduce` function is a utility function that returns a single value of type `Anything` based on a method of reduction. It accepts three parameters: the callable function that dictates how values will be combined, the list to combine into a single value, and the starting value. The starting value will dictate what type the `reduce` function returns. The following `smartAdd` functions makes uses of `reduce` to add according to a specific set of rules:

```ocellusscript
smartAdditionHelper takes Integer and Integer returns Integer
smartAdditionHelper x y = y % 3 == 0
                            ? x + (y * 4)
                            : x + y

smartAdd takes [Integer] returns Integer
smartAdd list = reduce smartAdditionHelper list 0
```

Again, note that `smartAdditionHelper` is _not_ called inside of the `smartAdd` function as `reduce` calls this automatically when running.

Below is the implementation for `reduce`:
```ocellusscript
reduce takes (Callable takes Anything and Anything returns Anything) \
    and [Anything] and Anything returns Anything
reduce f x s = helper f x s where
                helper combinator [] s = s
                helper combinator i s = combinator i s
                helper combinator (i:j) s = helper combinator j (combinator i s)
```

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