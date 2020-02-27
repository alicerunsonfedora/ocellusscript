# Using Efficacy CLI

The Efficacy compiler and interactive environment can be called from the terminal by running `efficacy.`

## Arguments

The following are arguments that can be passed to Efficacy to specify details. Running Efficacy without any arguments opens the interactive mode.

| Argument | Full Argument | Required | Description |
| -------- | ------------- | -------- | ----------- |
| `-i` | `--input` | No[^1] | The path to the input file to compile |
| `-o` | `--output` | No | The path to where the compiled executable will be placed |
| `-oT` | `--output-tokens` | No | The path to where the token file will be placed |

## Creating a Token File

Efficacy supports creating a JSON file containing the tokens it discovered while tokenizing the input file. It mainly contains a list of objects with the token type (see [Lexical Elements](../../language/11-spec/#lexical-elements)) and the token itself:

```json
[
    { "Identifier": "x" },
    { "Symbol": "=" },
    { "Identifier": "x" },
    { "Symbol": "+" },
    { "IntConstant": "5" },
]
```

This token file is useful when comparing a lexer's ability to tokenize an OcellusScript file to Efficacy's lexer, `OSTokenizer`.

[^1]: The `input` argument is required when compiling files or preparing a tokenized or parsed JSON file.