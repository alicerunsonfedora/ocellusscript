# Custom Types and Optionals

OcellusScript supports writing custom data types and types that inherit basic types. This can often be used to represent trees or a specific type of data.

The `type` function can be used to define a new type that is inherited from any of the [basic types](./01-expressions.md):

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

## Optional Types

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