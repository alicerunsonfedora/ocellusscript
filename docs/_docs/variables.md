---
title: Variables
layout: documentation
---

Variables are containers that contain information of a single type. Variables are often used to store information for later use.

## Variable Types

OcellusScript has a few basic types that are recognized by any compiler/interpreter:

- `Char`: A single Unicode character (includes letters and characters such as newline) surrounded by a pair of single quotes (`'e'`)
- `String`: A list of characters surrounded by a pair of quotation marks (`"cat"`)
- `Integer`: A whole number (`5129`)
- `Float`: A number as a decimal (`18.6`)
- `Boolean`: A toggle-able type that either contains `true` or `false`
- `Callable`: A type dedicated to functions that can be called
- `Anything`: A bare type used to indicate a variable containing any of the aforementioned types
- `Nothing`: A void type, usually represented as `null` in other languages

Variables can also accept types defined by the `type` and `shadowtype` statements.

## Creating variables

Creating a variable is achieved with the `var` or `let` statement:

```
var x = 1;
```

In this instance, we've created a variable `x` that holds the integer `1`. OcellusScript has already determine the type via type inference, but we can always explicitly state the type:

```
var x: Integer = 1;
```