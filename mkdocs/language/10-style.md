# Stylebook

While it isn't functionally necessary to follow the OcellusScript style guidelines, these guidelines can help make your code more readable and easier to understand.

## Keep Lines Short

A line in OcellusScript should be no more than 100 characters in length so that it can be opened and read easily without the need for text-wrapping.

## Always Include Type Signatures and Docstrings

Type signatures and docstrings are completely optional, but should be included to reduce confusion of input and output types, as well as providing sufficient documentation that can be called with `help`.

## Use Consistent Indentation

OcellusScript files should use space indents with a length of four spaces per indent.

## Put Conditionals and Operators on Separate Lines

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

## Indent Functions Defined with `where`

When possible, functions that use the `where` syntax to be defined on the next lines should be indented:

```ocellusscript
printLetters takes String returns Nothing
printLetters string = for 0 (length string) task where
                        task i = log string[i]
```

## Declare Private Functions and Types Before Functions

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