# Expressions and Basic Types

OcellusScript works like most programming languages and contains basic types:

- **Characters** are an individual alphanumeric or Unicode character wrapped in single quotes (example: `'\n'`).
- **Strings** are usually a [list](../04-lists/) of Characters wrapped in double quotes (example: `"Howdy"`).
- **Integers** are whole numbers (example: `5`).
- **Floats** are numbers that aren't exactly whole; rather, they may be a decimal or fraction (example: `3.141`).
- **Booleans** are a binary type that usually is either `true` (1) or `false` (0).

Likewise, there are other types in Ocellus:

- **Callables** are functions, expressions, or methods.
- **Nothing** is a void type to indicate a value of nothing. Usually comparable to `null` or `nil` in other languages. It is also the default type when no value is given in an [optional type](../05-types/#optional-types).
- **Anything** is also a void type, but is often used as a container type to describe any type.
- **Error** is a String-like type that disrupts program execution flow or requires special processing.

## Evaluating Expressions

OcellusScript is a functional language and mostly works off of expression evaluation. When expressions are evaluated, they will return a type and its result. Take a look at the following examples:

- `1 * 2` returns an Integer with a result of `2`.
- `"cat" + "dog"` returns a String with a result of `"catdog"`.
- `true or false` returns a Boolean with a result of `true`.

## Operators
The following operators can be used to evaluate an expression:

- `+` will add values. In the case of numbers, these will mathematically add up, while in the case of strings, these will concatenate the strings together.
- `-` will subtract values, usually only with numbers.
- `*` will multiply values, usually only with numbers.
- `/` will divide numbers. In the case of integers, these will try to divide it evenly and give the whole number with no remainder. For floats, this will return the whole number and its remainder.
- `%` will get the remainder of a division, usually use with integers.
- `==` will check if two values are equal to each other.