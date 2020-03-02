# The Hive Module

The Hive module is a standard library module that can be imported into OcellusScript scripts and modules with the `import` statement. The Hive module contains several useful functions, datatypes, and types.

!!! info "This document is incomplete"
    This document will be updated as more utilities are written into the Hive module.

## List Utilities

### `length`
```
length takes [Anything] returns Integer
```
Get the length of a list.

**Arguments**

- list: The list to gather the length of.

**Returns**: Integer value containing the length of the list, or 0 if the list is empty.

!!! example
    ```ocls
    length ["JavaScript", "Python", "CSS"]
    # 3
    ```

### `atPosition`
```
atPosition takes [Anything] and Integer returns Anything
```

Grab an item from the list at a specified position.

**Arguments**

- list: The list to iterate through
- position: The index of the item to return, if possible.

**Returns**: The item at the specified position, or Nothing.


!!! example
    ```ocls
    atPosition ["JS", "PY", "CSS"] 2
    # "CSS"
    ```

### `member`
```
member takes Anything and [Anything] returns Boolean
```
Determine whether an item is a member of a specified list.

**Arguments**

- item: The item to search for in the list
- list: The list to search for the member

**Returns**: Boolean value indicating whether the item is in the list.

!!! example
    ```
    member "Cheese" ["Bun", "Patty", "Cheese", "OtherBun"]
    # true
    ```

### `map`
```
map takes (Callable takes Anything returns Anything) and [Anything]\
    returns [Anything]
```

Create a list with a function applied to a set of elements.

**Arguments**

- fn: The function to apply to each element
- list: The list to apply the function to

**Returns**: A list with elements applied by the function

!!! example
    ```ocls
    allPlusOne = map (lambda x -> x + 1) [1, 2, 3]
    # [2, 3, 4]
    ```

### `filter`
```
filter takes (Callable takes Anything returns Boolean) and [Anything]\
    returns [Anything]
```

Create a list given a specific condition.

**Arguments**

- fn: The function to determine what items are inserted into the list
- list: The list to filter

**Returns**: A list filtered by the function

!!! example
    ```
    evens = filter (lambda x -> x % 2 == 0) [1, 2, 3, 4]
    # [2, 4]
    ```

### `reduce`
```
reduce takes (Callable takes Anything and Anything returns Anything)\
    and [Anything] and Anything\
    returns Anything
```
Combine a list into a single value.

!!! example
    ```
    plusTimesThree = reduce (lambda x, y -> (x + y) * 3) [1, 2, 3] 0
    # 54
    ```

**Arguments**

- fn: The function to determine how values are combined in the list
- list: The list to reduce into a single value
- value: The starting value

**Returns**: A single value from all of the combined values


## Iterators

### `for`
```
for takes Integer and Integer (Callable takes Anything? returns Anything?)\
    returns Nothing
```

Perform a task over a range.

**Arguments**

- start: The starting iteration value.
- end: The ending iteration value.
- task: The task to perform on each iteration.

!!! example
    ```ocls
    countToTen = for 1 4 task where
                task i = log i
    # 1
    # 2
    # 3
    # 4
    ```