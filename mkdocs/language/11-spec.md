# Specification

The following page contains technical information about OcellusScript. This information is useful for those wishing to write a custom compiler or interpreter for OcellusScript.

## Lexical Elements

During the tokenization process, OcellusScript will create tokens of the following types:

- `Keyword` refers to any of the primary keywords such as types, statements, and values.
- `Identifier` refers to a group of uppercase and lowercase letters.
- `StringConstant` refers to a string containing valid Unicode characters, excluding double quotes (unless escaped).
- `DocstringConstant` refers to a documentation string containing valid Unicode characters that start and end with a backtick (`\``).
- `CommentConstant` refers to a comment containing valid Unicode characters that start with the hash symbol (`#`) and end with a newline character (`\n`).
- `Symbol` refers to any non-alphanumeric characters.
- `IntConstant` refers to any integers that do not contain a decimal point.
- `FloatConstant` refers to a number that contains a single decimal point.

Below are the lists containing valid keywords, symbols, operators, etc.

| Type | Classified Elements |
| -- | -- |
| Keyword | `Character`, `String`, `Integer`, `Boolean`, `Float`, `Callable`, `Anything`, `Nothing`, `Error`, `import`, `module`, `where`, `takes`, `returns`, `log`, `only`, `except`, `warn`, `true`, `false`, `type`, `datatype`, `private` |
| Symbol | `<`, `>`, `,`, `?`, `[`, `]`, `(`, `)`, `-`, `=`, `+`, `*`, `/`, `%`, `\`, `!`, `:`, `#` |

## Grammar Structure

OcellusScript uses the following grammar set to define functions, expressions, types, etc. when parsing a list of tokens. Grammars with a pipe character (`|`) indicate an 'or' option, grammars with `?` will mean optional, and grammars with `*` will mean a group with zero or more of that particular group.

Expression grammars are organized in terms of precedence in ascending order (low --> high).

### Standard Expressions

The standard expression grammars are responsible for handling basic expressions such as `5 + 6` or `isOkay and isNotNull`.

| Grammar | Corresponding Tokens |
| ------- | -------------------- |
| expression | `functionReturn | (expression) ? (expression) : (expression) | booleanExpression` |
| booleanExpression | `equalityExpression 'and' equalityExpression | equalityExpression 'or' equalityExpression | 'not' equalityExpression | equalityExpression` |
| equalityExpression | `inequalityExpression == inequalityExpression | inequalityExpression != inequalityExpression | inequalityExpression` |
| inequalityExpression | `valueExpression > valueExpression | valueExpression < valueExpression | valueExpression` |
| valueExpression | `valueExpression + additiveExpression | valueExpression - additiveExpression | additiveExpression` |
| additiveExpression | `additiveExpression * multiplicativeExpression | additiveExpression - multiplicativeExpression | additiveExpression % multiplicativeExpression | multiplicativeExpression`
| multiplicativeExpression | `(expression) | StringConstant | IntegerConstant | FloatConstant | keywordConstant |` |
| optionalExpression | `(StringConstant | IntegerConstant | FloatConstant | keywordConstant) ?? (StringConstant | IntegerConstant | FloatConstant | keywordConstant)` |
| keywordConstant | `'true' | 'false' | 'Anything' | 'Nothing' | 'Error'` |

### Functions

The function grammars handle the grammars for defining functions with expressions.

| Grammar | Corresponding Tokens |
| ------- | -------------------- |
| `function` | `Identifier (signature)? (Docstring)? (Identifier*)? = (expression  | functionReturn)` |
| `functionReturn` | `Identifier (expression | Identifier)*` |
| `signature` | `Identifier 'takes' (typeList) 'returns' (typeList)` |
| `typeList` | `type ('and' type)* | type (',' type)*` |
| `type` | `('String' | 'Integer' | 'Float' | 'Character' | 'Error' | 'Anything' | 'Nothing' | 'Boolean' | 'Callable' | Identifier)('?')?` |

### Custom Declarations

| Grammar | Corresponding Tokens |
| ------- | -------------------- |
| typeDeclaration | `'type' Identifier '=' type` |
| datatypeDeclaration | `'datatype' Identifier '=' (Identifier)* ('or' (Identifier)*)*` |

### Modules

The module grammar handles defining modules. If a file does _not_ contain a module, a new module should be created with a random name.

| Grammar | Corresponding Tokens |
| ------- | -------------------- |
| module | `(importStatements)* ('module' Identifier 'where')? (function | typeDeclaration | datatypeDeclaration)*` |
| importStatements | `'import' Identifier (('only' | 'except') Identifier (',' Identifier)*)?` |