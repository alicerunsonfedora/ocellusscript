# Lexer

The `lexer` submodule of Efficacy contains all of the tools necessary to tokenize a string or a file into a a list of OcellusScript tokens.
## `OSTokenType`

An enumeration type for the different token types.

This enumeration class is used to differentiate between the different types of tokens used for OcellusScript parsing. The values of the enumerations correspond to the [lexical grammar names](../../language/11-spec.md#lexical-elements) for each type.

| Key | Corresponding Value |
| --- | ------------------- |
| `keyword` | Keyword |
| `identifier` | Identifier |
| `string` | StringConstant |
| `docstring` | DocstringConstant |
| `comment` | CommentConstant |
| `symbol` | Symbol |
| `num_integer` | IntConstant |
| `num_float` | FloatConstant |
| `operator` | Operator |

## `OSTokenizer`
The tokenizing class for OcellusScript.

The tokenizer is responsible for converting a stream of characters into OcellusScript tokens that can be used for parsing.

!!! example
    Below is an example of how `OSTokenizer` can be used to create a list of tokens from a string containing OcellusScript code.

    ```python
    from efficacy.lexer import OSTokenizer
    
    lexer = OSTokenizer(script="example x = x > 5 ? x + 6 : x + 8\n")
    tokens = lexer.tokenize()
    print(tokens[0]) # (<OSTokenType: OSTokenType.identifier>, "example")
    ```

### Attributes

- `source`: The list of characters that will be converted to tokens

### Methods

#### `__init__`
Initialize the tokenizer.
        
**Arguments**

- `script`: The script string to tokenize

#### `tokenize`
Generate a list of tokens from a given string.

**Returns**: A list containing the tokens as a tuple containing the token's type and the token itself.