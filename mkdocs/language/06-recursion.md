# Recursion

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

## `where` Expression

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