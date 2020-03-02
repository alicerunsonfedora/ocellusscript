# Lists and Pattern Matching

Another common type is a list. A list is a collection of items that can be iterated through. In Ocellus, lists works more like Haskell's list in the sense that they are nested pairs with a head and tail. For instance, take a look at the following list below:

```
[1, 2, 3, 4]
```

The following list in OcellusScript corresponds to the following:

```
1 : (2 : (3 : (4 : Nothing)))
```

Lists in OcellusScript always have a `Nothing` type as the inner-most tail, though the list can be of any type inside with any length.

Accessing a list is relatively straightforward using this syntax:

```
(first : second : rest)
```

Where `first` corresponds to the first item in the list, `second` refers to the second item, and `rest` refers to everything else after the first two elements. This syntax can be trimmed to refer to just the first item and the rest of the items, which may be useful in recursive cases:

```
(head : tail)
```

Where `head` refers to the first item and `tail` refers to everything after the fist item.

Additionally, referring to an item in a list without referencing pairs is relatively easy to do with the standard `list[index]` syntax where `index` is the position of the element in the list. Lists in OcellusScript start at position `0`.

## List Utilities

OcellusScript comes with some utility functions that work with lists to make things a bit easier. These utility functions accept a list of type `[Anything]` and return different values depending on the utility in question:

- `length list` will return an `Integer` that represents how many items are in a list.
- `member item list` will return a `Boolean` that indicates whether `item` is an element in `list`.
- `map func list` will return a list of `[Anything]` with the function `func` applied to it.
- `filter func list` will return a list of `[Anything]` based on if the items meet the condition defined in `func`.
- `reduce func list startingValue` will return a single value of type `Anything` based on a function `func` and staring with value `startingValue`.

The functions `map`, `filter`, and `reduce` are discussed in great detail in the [Higher-order Functions](./07-hoc.md) section, as well as the [Hive module documentation](./12-hive.md#list-utilities).

Lists can also be added/concatenated using the standard `+` operator, and `-` will remove the first instance of an element:

```ocellusscript
addList takes Nothing returns [Integer]
addList = [1, 2] + [3] # returns [1, 2, 3]

removeList takes Nothing returns [Integer]
removeList = [1, 2, 3, 2] - [2] # returns [1, 3, 2]
```

## Pattern Matching

Likewise, functions in OcellusScript can also cover multiple cases based on a common pattern in the input parameters. Each definition will attempt to match a specific type of pattern, so it's recommended that functions define all types of patterns that are necessary. For instance, the `butFirst` function below will account for empty lists, lists with one item, and lists with multiple items:

```ocellusscript
butFirst takes [Anything] returns [Anything]
butFirst [] = []
butFirst [x] = [x]
butFirst (head:tail) = tail
```

Note that there are three definitions listed:

- `butFirst []` will match for empty lists specifically
- `butFirst [x]` will match for lists that contain only one item
- `butFirst (head:tail)` will match for lists that contain a head and a tail.

Pattern matching works in OcellusScript regardless of the input type. For instance, take a look at the following function `isEven` which determines whether an optional integer is even or not:

```ocellusscript
isEven takes Integer? returns Boolean
isEven Nothing = false
isEven number = number % 2 == 0
```

It is important to note that OcellusScript will match patters in the order that they are defined in. In the case of `isEven`, the function will attempt to match the pattern `isEven Nothing` before matching the pattern `isEven number`.

OcellusScript patterns can ignore certain information by replacing it with an underscore, like below:

```ocellusscript
butFirst (_ : tail) = tail
```

Where OcellusScript will ignore the head of the list pair.