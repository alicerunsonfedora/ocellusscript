# Parser

The `parser` submodule of Efficacy contains all of the tools necessary to parse a list of tokens into an abstract syntax tree to be used for compilation or additional processing.

## `OSParserError`

The base error to use when the parser has failed.

## `OSParser`

The parsing class for OcellusScript.

The parser is responsible for reading a list of tokens and converting the them into a traversable abstract syntax tree that can be used to compile into a program with LLVM or can be processed differently with a Python script.

!!! example
    The following is an example of how the parser can be used to create the abstract syntax tree.

    ```py
    from efficacy.parser import OSParser
    example_src = """module Example where

    example takes Nothing returns Integer
    example = 5"""

    parsed = OSParser(script=example_src).parse()
    print(parsed)
    ```

### Methods

#### `__init__`
Initialize the OcellusScript Parser object.

**Keyword Arguments**
- `script`: The string containing the code to parse. The parser will tokenize this script before parsing it.
- `tokens`: The pre-processed list of tokens to use for parsing.

#### `parse`
Parse the list of tokens and return an abstract syntax tree.

**Arguments**

- `skip_new_line`: Whether to skip the newline token (`LineReturn`). Defaults to `True`.

**Returns**: A JSON-like dictionary containing all of the parsed functions, expression, and modules.

**Raises**: OSParserError if there's an error in the syntax of the current token being processed.