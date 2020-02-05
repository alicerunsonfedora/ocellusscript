# OcellusScript Language Specifications

The following document describes the specifications and language features of OcellusScript and how they should operate; this document is useful for those wishing to make compilers, interpreters, etc.

## Lexical Elements

During the tokenization process, OcellusScript will create tokens of the following types:

- `Keyword` refers to any of the primary keywords such as types, statements, and values.
- `Identifier` refers to a group of uppercase and lowercase letters.
- `StringConstant` refers to a string containing valid Unicode characters, excluding double quotes (unless escaped).
- `DocstringConstant` refers to a docstring containing valid Unicode characters that start and end with a backtick (`\``).
- `CommentConstant` refers to a comment containing valid Unicode characters that start with the hash symbol (`#`) and end with a newline character (`\n`).
- `Symbol` refers to any non-alphanumeric characters.
- `IntConstant` refers to any integers that do not contain a decimal point.
- `FloatConstant` refers to a number that contains a single decimal point.
- `Operator` refers to any symbol used for operations and logical operators like `and`.

Below are the lists containing valid keywords, symbols, operators, etc.

| Type | Classified Elements |
| -- | -- |
| Keyword | `Character`, `String`, `Integer`, `Boolean`, `Float`, `Callable`, `Anything`, `Nothing`, `Error`, `import`, `module`, `where`, `takes`, `returns`, `log`, `only`, `except`, `warn`, `true`, `false`, `type`, `datatype`, `private` |
| Symbol | `<`, `>`, `,`, `?`, `[`, `]`, `(`, `)`, `-`, `=`, `+`, `*`, `/`, `%`, `\`, `!`, `:`, `#` |
| Operator | `<`, `>`, `-`, `+`, `*`, `/`, `%`, `=`, `>=`, `<=`, `==`, `and`, `not`, `or` |