<div align="center">
    <img width="128" src="./logo.png" alt="OcellusScript logo">
    <h1>NOC</h1>
</div>

The **NOC** is the official OcellusScript compiler. NOC is a Kotlin-implemented package that contains libraries, as well as executables for JVM and WebAssembly.

## Getting Started

### Requirements

- JDK v1.8
- Gradle
- IDE that supports Kotlin

After cloning the OcellusScript repository, navigate to the `compiler` directory and then run `gradlew.bat build` if on Windows or `gradlew build` on macOS/Linux.

> Note: you may need to set the executable permission on `gradlew` if it doesn't exist already.

## Roadmap

This is the current roadmap for NOC:

- [X] Tokenizer
- [ ] Parser
    - [X] Imports
    - [X] Module names
    - [X] Custom types
    - [X] Shadow types
    - [X] Variable declarations
    - [ ] Expression parsing
        - [X] Primitive types
        - [ ] Lists
            - [ ] List literals (`[1, 2, 3, 4]`)
            - [ ] Element with list literal (`list[2]``)
        - [ ] Function calls
        - [X] Nested expressions
    - [ ] Class declarations
    - [ ] Function declarations
        - [ ] Function signature
        - [ ] Function definition
    - [ ] Symbol table generator
- [ ] JVM command line
    - [X] Arguments
    - [X] Creating token files
    - [X] Creating parse files
    - [ ] Creating compiled bytecode files
    - [ ] Creating an executable JAR in Gradle
- [ ] Java libraries
    - [ ] Executable JAR
- [ ] Web assembly libraries
    - [ ] Compiled WASM file
- [ ] Class modules
    - [ ] Lists
    - [ ] Strings
    - [ ] Utilities/higher-order functions

## Found an issue?

Issues for NOC can be reported on YouTrack. [File a bug report &rsaquo;](https://youtrack.marquiskurt.net/youtrack/newIssue?project=NOC)