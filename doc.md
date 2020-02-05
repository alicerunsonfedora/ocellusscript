# The OcellusScript Programming Language

## What is OcellusScript?

OcellusScript is a functional programming language, originally designed to work hand-in-hand with the coding mini game from the Unscripted visual novel. OcellusScript heavily draws inspiration and syntax from languages like Haskell, Swift, JavaScript/ES5, and Python. OcellusScript aims to be an easy-to-use, type safe, and powerful language.

## Documentation

The following document describes the capabilities of OcellusScript and how to get started writing programs in OcellusScript. More information on the specifications of OcellusScript can be found in the [specification document](spec.md).

### Expressions and Basic Types

OcellusScript works like most programming languages and contains basic types:

- **Characters** are an individual alphanumeric or Unicode character wrapped in single quotes (example: `'\n'`).
- **Strings** are usually a [list](#lists-and-pattern-matching) of Characters wrapped in double quotes (example: `"Howdy"`).
- **Integers** are whole numbers (example: `5`).
- **Floats** are numbers that aren't exactly whole; rather, they may be a decimal or fraction (example: `3.141`).
- **Booleans** are a binary type that usually is either `true` (1) or `false` (0).

Likewise, there are other types in Ocellus:

- **Callables** are functions, expressions, or methods.
- **Nothing** is a void type to indicate a value of nothing. Usually comparable to `null` or `nil` in other languages. It is also the default type when no value is given in an [optional type](#optional-types).
- **Anything** is also a void type, but is often used as a container type to describe any type.
- **Error** is a String-like type that disrupts program execution flow or requires special processing.

#### Evaluating Expressions

OcellusScript is a functional language and mostly works off of expression evaluation. When expressions are evaluated, they will return a type and its result. Take a look at the following examples:

- `1 * 2` returns an Integer with a result of `2`.
- `"cat" + "dog"` returns a String with a result of `"catdog"`.
- `true or false` returns a Boolean with a result of `true`.

#### Operators
The following operators can be used to evaluate an expression:

- `+` will add values. In the case of numbers, these will mathematically add up, while in the case of strings, these will concatenate the strings together.
- `-` will subtract values, usually only with numbers.
- `*` will multiply values, usually only with numbers.
- `/` will divide numbers. In the case of integers, these will try to divide it evenly and give the whole number with no remainder. For floats, this will return the whole number and its remainder.
- `%` will get the remainder of a division, usually use with integers.
- `==` will check if two values are equal to each other.

### Defining Functions (Callables)

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

####  Function are Not Variables

It is important to keep in mind that writing functions in OcellusScript does not mean that they are variables. Any function definition is a Callable that usually returns a value. For instance, the following might look like a variable assignment in Python:

```ocellusscript
helloWorld = "Hello, world!"
```

When, in fact, this is _not_ a variable. This is a parameterless function that returns the evaluation of the string `"Hello, world!"`.


#### Type Signatures

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

#### Callables as Parameters in a Type Signature

There may be cases where a function itself is passed into another function as a parameter, like in [higher-order functions](#higher-order-functions). To accomodate for this, the type signature can be modified to indicate that it takes a function (`Callable`) with its own parameters and return type. Take a look at the example below:

```ocellusscript
test takes (Callable takes Integer returns Integer) \
    and Integer returns Integer
```

### Conditionals

Often, you'll need to compare two values to each other and use its comparison. These conditional operators can be used in expression evaluation:

- `==` will determine whether two values are equal to each other.
- `!=` will determine whether two values are _not_ equal to each other.
- `<` will determine whether the first value is less than the second value.
- `>` will determine whether the first value is greater than the second value.
- `<=` will determine whether the first value is less than or equal to the second value.
- `>=` will determine whether the first value is greater than or equal to the second value.

It's important to note that comparisons are usually type inclusive, meaning that the types are also compared. `"2" == 2` will always evaluate to `false` since the types are different, but `2 == 2` will always evaluate to `true` because the types are the same.

Comparisons will _always_ return a boolean value.

#### Boolean operators
Comparisons and conditions can work with each other using boolean operators:

- `and` determines whether both the first value and the second value will evaluate to `true`.
- `not` will take the opposite conditional value (i.e. `true` to `false`).
- `or` determines whether either the first value or the second value will evaluate to `true`.

#### Working with Conditionals

The ternary operator syntax is used to determine what to further evaluate or return based on a condition. The typical syntax is as follows:
```ocellusscript
condition
    ? (expression to evaluate if condition)
    : (expression to evaluate if not condition)
```

The following is also valid syntax:
```ocellusscript
condition ? true : false
```

so, for example, the following will make a log entry depending on what gets passed into the function `warnForVillain`:

```ocellusscript
warnForVillain name = isVillain name
                        ? warn "Careful! " + villain + " is a villain."
                        : log "You're safe." 
```

### Lists and Pattern Matching

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

#### List Utilities

OcellusScript comes with some utility functions that work with lists to make things a bit easier. These utility functions accept a list of type `[Anything]` and return different values depending on the utility in question:

- `length list` will return an `Integer` that represents how many items are in a list.
- `member item list` will return a `Boolean` that indicates whether `item` is an element in `list`.
- `map func list` will return a list of `[Anything]` with the function `func` applied to it.
- `filter func list` will return a list of `[Anything]` based on if the items meet the condition defined in `func`.
- `reduce func list startingValue` will return a single value of type `Anything` based on a function `func` and staring with value `startingValue`.

The functions `map`, `filter`, and `reduce` are discussed in great detail in the [Higher-order Functions](#higher-order-functions) section.

Lists can also be added/concatenated using the standard `+` operator, and `-` will remove the first instance of an element:

```ocellusscript
addList takes Nothing returns [Integer]
addList = [1, 2] + [3] # returns [1, 2, 3]

removeList takes Nothing returns [Integer]
removeList = [1, 2, 3, 2] - [2] # returns [1, 3, 2]
```

#### Pattern Matching

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

### Custom Types and Optionals

OcellusScript supports writing custom data types and types that inherit basic types. This can often be used to represent trees or a specific type of data.

The `type` function can be used to define a new type that is inherited from any of the [basic types](#Expressions-and-Basic-Types):

```ocellusscript
type Side = Float
type Radius = Float
```

Where `Side` and `Radius` is a type that is inherited from the `Float` type. 

Likewise, defining custom data types is accomplished with the `datatype` function:

```ocellusscript
datatype Shape = Rectangle Side Side 
                    or Ellipse Radius Radius
```

Where `Shape` can now either be a data type of `Rectangle` with parameters `Side` and `Side` or a data type of `Ellipse` with parameters `Radius` and `Radius`.

OcellusScript will work with custom types and data types as standard types in functions, which is useful in pattern matching cases. The following `area` function matches across different type patterns to calculate a shape's area:

```ocellusscript
area takes Shape returns Float
area (Rectangle x y) = x * y
area (Ellipse r q) = pi * r * q
```

Data types are often useful for creating custom types with specific attributes or for creating tree-like structures. For instance, the following code includes a custom tree data type and a function to collapse a tree into a single value with pattern matching:

```ocellusscript
datatype NumberTree = Leaf Integer
                        or Branch Integer NumberTree NumberTree

collapseTree takes NumberTree returns Integer
collapseTree (Leaf n) = n
collapseTree (Branch n x y) n + (collapseTree x) + (collapseTree y)

sampleTree = Branch 0 (Leaf 6) (Branch 1 (Leaf 2) (Leaf 9))

collapsedSample = collapseTree sampleTree
```

Note that in the pattern `collapseTree (Branch n x y)`, the function calls upon itself to collapse the subtrees `x` and `y`. OcellusScript support different types of recursion and allows for this kind of behavior.

#### Optional Types

OcellusScript also support types that may contain a specific type of value or `Nothing`. These types, known as `optionals`, are often used in cases where the type of data being returned is unclear. Optional types are denoted by `?` at the end of the type. For instance, the following function `getDefaultHealth` will return an integer or a default value if `Nothing` is received.

```ocellusscript
getDefaultHealth takes Integer? returns Integer
getDefaultHealth health = health ?? 100
```

The `??` operator in the expression indicates that the following value should be used if the preceding value is of type `Nothing`. Similarly, this function can be rewritten using pattern matching to make this clearer:

```ocellusscript
getDefaultHealth takes Integer? returns Integer
getDefaultHealth Nothing = 100
getDefaultHealth health = health
```

Currently, functions that use optional types _must_ account for when a type returns `Nothing` instead of the intended value and does not support force unwrapping. However, this behavior can be replicated (if desired) with a sample utility function like the one below:

```ocellusscript
datatype ForcedValue = Anything or Error

forceUnwrap takes Anything? returns ForcedValue
forceUnrwap value = value ?? Error "Cannot unwrap value Nothing."
```

### Recursion, `where`, Higher-order Functions, and Lambda Functions

OcellusScript supports different types of recursion and are relatively easy to implement. The most typical form of recursion used in OcellusScript is linear recursion and works by processing a single element and constantly working on elements until the innermost element returns a single value. Elements then work upwards to "collapse" the work into a single evaluation. For instance, the following function below will keep working until the element value in question is divisible by 2:

```ocellusscript
myEquation takes Integer returns Integer
myEquation n = n % 2 == 0
                ? n + 5
                : myEquation (n * 2)
```

The following would be how OcellusScript processes `myEquation` with the input parameter being `5`:

```
Start with myEquation n where n = 5.
Check if n is divisible by 2.
    n is NOT divisible by 2, so we multiply n by 2.
    New n = 10.
    Evaluate myEquation where n = 10.
    Check if n is divisible by 2.
        n IS divisible by 2, so we evaluate n + 5.
        n + 5 is 15.
        Return back value 15.
    Evaluation returns 15.
Evaluation returns 15.
```

#### `where` Expression

Sometimes, it might be impractical to work with recursion and pattern matching all in a single function. To mitigate this, a helper function can be defined with the `where` expression. The following function `reverse` uses the `where` expression to write a pattern matching function that then can get used recursively.

```ocellusscript
reverse takes String returns String
reverse word = reverseHelper word "" where
                reverseHelper [] newWord = newWord
                reverseHelper character newWord = newWord + [character]
                reverseHelper (firstChar : otherChars) = reverseHelper 
                                                            otherChars
                                                            (newWord + [firstChar])

```

The helper function `reverseHelper` gets called recursively when dealing with strings of more than one character in length and will transfer the letters over to `newWord`. After evaluating `reverseHelper`, the return value is returned to the original function.

The `where` expression can be used to define a function preceding it or a specific value and is often used in cases of tail recursion or when pattern matching is needed. Note that the type signature for `reverse` does not include the signature for `reverseHelper` as it is not required.

#### Higher-order Functions

OcellusScript supports writing functions that will accept functions as parameters. These functions, called higher-order functions, will usually take a function as one of its inputs or return a function as its output. OcellusScript comes with some built-in higher-order functions for use with iteration and lists.

##### `for`

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

##### `map`

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

##### `filter`

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

##### `reduce`

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

#### Lambda Functions

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

### Error Handling

There may be functions that are defined in OcellusScript that might return an `Error` type and stop program flow. As a way to gracefully handle errors, the ternary-like `!` operator syntax can be used. The following example code works with the forced unwrapped value code from the [Optional Types](#optional-types) section to handle error handling:

```ocellusscript
addForcedValues takes ForcedValue returns Integer?
addForcedValues x = (forceUnwrap x)
                        ! x + 5
                        : log "Couldn't unwrap value x"
```

### Modules and Main Execution

OcellusScript works on a file-based level and supports creating and importing modules that contain other functions and utilities. When an OcellusScript file is written, it is considered a module in and of itself when the `module` function is defined. The following example in the file **vill.ocls** shows how a module is written:

```ocellusscript
module VillainDatabase where

type Reform = Boolean
type Name = String

datatype KnownVillain = Villain Name Reform

knownVillains takes Nothing returns [KnownVillains]
knownVillains = [(Villain "Nightmare Moon" true),
                 (Villain "Discord" true),
                 (Villain "Tirek" false),
                 (Villain "Tempest Shadow" false),
                 (Villain "Starlight Glimmer" false),
                 (Villain "Chrysalis" false)]

knownByReform takes Nothing returns [KnownVillains]
knownByReform = filter
                    (lambda (Villain _ reform) -> reform)
                    knownVillains

inVillainDatabase takes String returns Boolean
inVillainDatabase name = member
                            name
                            (map (lambda (Villain name _ ) -> name) knownVillains)
```

**vill.ocls** is a typical OcellusScript file, but because the `module` function is defined at the top, all functions and types in this file are publicly accessible to other OcellusScript files by importing `VillainDatabase`. For example, another file called **chr.ocls** can make use of everything inside this module by using the `import` function:

```ocellusscript
import VillainDatabase

foundChrysalis takes Nothing returns Boolean
foundChrysalis = inVillainDatabase "Chrysalis"
```

#### Specific imports

Importing the entire module may not be necessary and could cost performance. OcellusScript can handle this with specific imports. Again, with **chr.ocls**, we can manually import the `inVillainDatabase` function without importing everything else with the `only` statement:

```ocellusscript
import VillainDatabase only inVillainDatabase

foundChrysalis takes Nothing returns Boolean
foundChrysalis = inVillainDatabase "Chrysalis"
```

Likewise, `except` will import the entire module except a specific function:

```ocellusscript
import VillainDatabase except knownByReform

foundChrysalis takes Nothing returns Boolean
foundChrysalis = inVillainDatabase "Chrysalis"
```

#### Private functions

Modules expose every function and type in a file and make it publicly accessible, which may not be desired. To mitigate this, adding the keyword `private` in front of a function definition will make sure that the function does _not_ get imported when the module is imported.

Looking back at **vill.ocls**, we could probably make the `knownVillains` function private so, say, a villain can't delete their entry from the database:

```ocellusscript
module VillainDatabase where

type Reform = Boolean
type Name = String

datatype KnownVillain = Villain Name Reform

knownVillains takes Nothing returns [KnownVillains]
private knownVillains = [(Villain "Nightmare Moon" true),
                 (Villain "Discord" true),
                 (Villain "Tirek" false),
                 (Villain "Tempest Shadow" false),
                 (Villain "Starlight Glimmer" false),
                 (Villain "Chrysalis" false)]

knownByReform takes Nothing returns [KnownVillains]
knownByReform = filter
                    (lambda (Villain _ reform) -> reform)
                    knownVillains

inVillainDatabase takes String returns Boolean
inVillainDatabase name = member
                            name
                            (map (lambda (Villain name _ ) -> name) knownVillains)
```

Note that the `private` keyword does _not_ need to be in the type signature of the function.

#### Documentation Strings and Comments

It's good practice to include documentation with your source code. Documentation often provides information on what a function will do or what a module contains. Documentation strings (docstrings) are denoted with a set of backticks (`\``) can be inserted between a type signature and a function definition like below:

```ocellusscript
inVillainDatabase takes String returns Boolean
`Check whether a villain is in the known villain database.

Arguments:
    name: The name of the person to search for.
`
inVillainDatabase name = member
                            name
                            (map (lambda (Villain name _ ) -> name) knownVillains)
```

If you want to write comments or notes in a file, you can use a single hash (`#`) and then keep typing. OcellusScript will not execute any code in triple-quotes or after a hash. Comments with a hash extend until the next line in a file.

To access documentation for a function, the `help` function can be called:

```ocellusscript
help inVillainDatabase
```

Where `help` accepts a single parameter, the callable function with a docstring. If no documentation is found, nothing is returned.

#### Executing a File

Thus far, we've defined functions in OcellusScript but haven't quite interacted with them. There are two ways to interact with them:

- Importing the module into an interactive interpreter environment
- Defining a `main` function that will be executed when running a compiled version of a script

OcellusScript supports the `main` function to write a function that executes when you call on a file's executable:

```ocellusscript
import VillainDatabase

main args = log (inVillainDatabase "Twilight")
```

When the file above is run after compiling, the `main` function will be executed. The following is the type signature of the `main` function:

```ocellusscript
main takes [String?] returns Anything?
```

When the file is executed, it can take in parameters from the command line as parameters to `main`.

### General Style Guidelines

While it isn't functionally necessary to follow the OcellusScript style guidelines, these guidelines can help make your code more readable and easier to understand.

#### Keep Lines Short

A line in OcellusScript should be no more than 100 characters in length so that it can be opened and read easily without the need for text-wrapping.

#### Always Include Type Signatures and Docstrings

Type signatures and docstrings are completely optional, but should be included to reduce confusion of input and output types, as well as providing sufficient documentation that can be called with `help`.

#### Use Consistent Indentation

OcellusScript files should use space indents with a length of four spaces per indent.

#### Put Conditionals and Operators on Separate Lines

While it is possible to do an in-line ternary operator for a conditional, if the condition evaluation is lengthy, consider putting them on separate lines:

```ocellusscript
doStuff takes Integer returns Integer
doStuff x = x % 5 == 1
                ? x + 13
                : x + 5
```

This should also be applied with operators and lists, if necessary:

```ocellusscript
type Name = String
datatype Equestrian = Pony Name
                        or Changeling Name
                        or Dragon Name
                        or Yak Name
                        or Zebra Name

myList = [(Changeling "Ocellus"),
          (Pony "Twilight"),
          (Zebra "Zecora")]
```

This should additionally be applied with parameters of functions, if necessary:

```ocellusscript
inVillainDatabase name = member
                            name
                            (map (lambda (Villain name _ ) -> name) knownVillains)
```

If needed, the `\` operator at the end of a line can be used to break up other components like type signatures:

```ocellusscript
for takes Integer and Integer and \
    (Callable takes Anything? returns Anything?) returns Nothing
```

#### Indent Functions Defined with `where`

When possible, functions that use the `where` syntax to be defined on the next lines should be indented:

```ocellusscript
printLetters takes String returns Nothing
printLetters string = for 0 (length string) task where
                        task i = log string[i]
```

#### Declare Private Functions and Types Before Functions

When possible, any custom types, data types, and private functions should go before public functions:

```ocellusscript
module Equestria where

type Name = String
datatype Equestrian = Pony Name
                        or Changeling Name
                        or Dragon Name
                        or Yak Name
                        or Zebra Name

private testList = [(Changeling "Ocellus"),
                    (Pony "Twilight"),
                    (Zebra "Zecora")]

main args = log "Imported!"
```