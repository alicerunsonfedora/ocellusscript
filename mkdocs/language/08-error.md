# Error Handling

There may be functions that are defined in OcellusScript that might return an `Error` type and stop program flow. As a way to gracefully handle errors, the ternary-like `!` operator syntax can be used. The following example code works with the forced unwrapped value code from the [Optional Types](../05-types/#optional-types) section to handle error handling:

```ocellusscript
addForcedValues takes ForcedValue returns Integer?
addForcedValues x = (forceUnwrap x)
                        ! x + 5
                        : log "Couldn't unwrap value x"
```