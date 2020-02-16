# Conditionals

Often, you'll need to compare two values to each other and use its comparison. These conditional operators can be used in expression evaluation:

- `==` will determine whether two values are equal to each other.
- `!=` will determine whether two values are _not_ equal to each other.
- `<` will determine whether the first value is less than the second value.
- `>` will determine whether the first value is greater than the second value.
- `<=` will determine whether the first value is less than or equal to the second value.
- `>=` will determine whether the first value is greater than or equal to the second value.

It's important to note that comparisons are usually type inclusive, meaning that the types are also compared. `"2" == 2` will always evaluate to `false` since the types are different, but `2 == 2` will always evaluate to `true` because the types are the same.

Comparisons will _always_ return a boolean value.

## Boolean operators
Comparisons and conditions can work with each other using boolean operators:

- `and` determines whether both the first value and the second value will evaluate to `true`.
- `not` will take the opposite conditional value (i.e. `true` to `false`).
- `or` determines whether either the first value or the second value will evaluate to `true`.

## Working with Conditionals

The ternary operator syntax is used to determine what to further evaluate or return based on a condition. The typical syntax is as follows:
```ocellusscript
(condition)
    ? (expression to evaluate if condition)
    : (expression to evaluate if not condition)
```

The following is also valid syntax:
```ocellusscript
condition ? true : false
```

so, for example, the following will make a log entry depending on what gets passed into the function `warnForVillain`:

```ocellusscript
warnForVillain name = (isVillain name)
                        ? (warn "Careful! " + villain + " is a villain.")
                        : (log "You're safe.")
```