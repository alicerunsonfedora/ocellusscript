# Current Progress

!!! warning
    OcellusScript is a work-in-progress language, so not all components of OcellusScript are functional. Below is a running checklist of what has been completed and what still needs to be worked on.

## Language Specification

The language specification checklist contains all of the necessary information on how OcellusScript is defined as a language. This includes lexical elements, grammars, evaluations, etc.

- [X] Lexical elements
- [X] Language grammar structure
    - [X] Module grammars
    - [X] Custom type/datatype grammars
    - [X] Function definition grammars
    - [X] Expression grammars
    - [ ] Function call grammars

!!! note
    Language grammars may be updated as Efficacy's parser is developed to better represent itself.

## Efficacy

Efficacy is the official lexer, parser, compiler and interpreter for OcellusScript.

- [X] Lexer
- [ ] Parser
    - [X] Modules
    - [X] Custom types
    - [X] Custom datatypes
    - [X] Basic expressions
    - [ ] Function calls
    - [ ] Conditional and null expressions
    - [X] Function definitions
- [ ] Compiler
- [ ] Command Line
    - [X] Reading input files
    - [X] Creating token JSON files
    - [X] Creating abstract syntax tree JSON files
    - [ ] Creating compiled files
    - [ ] Interactive environment