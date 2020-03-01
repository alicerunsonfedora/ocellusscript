# Specification

The following page is the specification for the OcellusScript language and contains technical information such as lexical elements, program structure, and parsing grammars. Developers using OcellusScript don't need to be too concerned with the specification, but this document is useful for those wishing to write an implementation of the OcellusScript specification, either as a compiler/interpreter for OcellusScript or or as a new language that stems from this spec.

## Lexical Elements

During the tokenization process, OcellusScript will create tokens of the following types:

- `Keyword` refers to any of the primary keywords such as types, statements, and values.
- `Identifier` refers to a group of uppercase and lowercase letters.
- `StringConstant` refers to a string containing valid Unicode characters, excluding double quotes (unless escaped).
- `DocstringConstant` refers to a documentation string containing valid Unicode characters that start and end with a back tick (`).
- `CommentConstant` refers to a comment containing valid Unicode characters that start with the hash symbol (`#`) and end with a newline character (`\n`).
- `Symbol` refers to any non-alphanumeric characters.
- `IntConstant` refers to any integers that do not contain a decimal point.
- `FloatConstant` refers to a number that contains a single decimal point.
- `LineReturn` refers to a newline character (`\n`).

Below are the lists containing valid keywords, symbols, operators, etc.

| Type | Classified Elements |
| -- | -- |
| Keyword | `Character`, `String`, `Integer`, `Boolean`, `Float`, `Callable`, `Anything`, `Nothing`, `Error`, `import`, `module`, `where`, `takes`, `returns`, `log`, `only`, `except`, `warn`, `true`, `false`, `type`, `datatype`, `private`, `and`, `or`, `not` |
| Symbol | `<`, `>`, `,`, `?`, `[`, `]`, `(`, `)`, `-`, `=`, `+`, `*`, `/`, `%`, `\`, `!`, `:`, `#` |

### Notes on Lexical Elements

- `CommentConstant` is not required to be listed or parsed and can be removed, if necessary.

## Grammar Structure

OcellusScript uses the following grammar set to define functions, expressions, types, etc. when parsing a list of tokens. Grammars with a pipe character (`|`) indicate an 'or' option, grammars with `?` will mean optional, and grammars with `*` will mean a group with zero or more of that particular group.

### Modules

!!! info "Grammar"
    ```
    module := (importStatement)* (module Identifier where)? (fnDef | dataDef | typeDef)*
    importStatement := import Identifier ((except | only) Identifier (, Identifier)*)?
    ```

#### Module Names

In cases where there isn't a module statement in the file or script, a random name is assigned and the module is marked as not importable. Otherwise, the module's name will be assigned from the module statement and will be marked as importable.

#### Import Statements
When import statements are parsed, the import names in the abstract syntax tree will be represented in three ways:

- `Module.*`, when importing the entire module
- `Module.specific`, when importing `specific` from `Module`
- `Module!specific`, when importing the entire module except for `specific`


### Custom Types and Datatypes

!!! info "Grammar"
    ```
    dataDef := datatype Identifier = dataStructDef (or dataStructDef)*
    dataStructDef := (Identifier (Identifier | Keyword)*)
    typeDef := type Identifier = Keyword
    ```

#### Identifiers in Datatypes and Custom Types

OcellusScript requires that the identifiers used to define custom datatypes and types be written in `PascalCase` to prevent possible confusion with other functions.

### Functions

!!! info "Grammar"
    ```
    fnDef := (fnSignature)? (Docstring)? fnBody (fnBody)*
    fnSignature := Identifier takes (fnSignatureType)* returns fnSignatureType
    fnSignatureType := [Identifier | Keyword] | Identifier|Keyword(?)? | (fnSignature)
    fnBody := Identifier (fnParam)* = (fnResult)
    fnParam := Identifier | fnLikeData | fnWithCons
    fnLikeData := (Identifier (Identifier | Keyword | IntConstant | StringConstant)*)
    fnWithCons := (Identifier : Identifier (: Identifier)*)
    fnResult := expression*
    ```

### Expressions

!!! info "Grammar"
    ```
    expression := boolExpr | expression
    boolExpr := equExpr (and | or) equExpr | not equExpr | equExpr
    equExpr := lowIneqExpr ((! | =)=) lowIneqExpr | lowIneqExpr
    lowIneqExpr := highIneqExpr ((> | <)=) highIneqExpr | highIneqExpr
    highIneqExpr := addExpr (> | <) addExpr | addExpr
    addExpr := multExpr (+ | -) multExpr | multExpr
    multExpr := term (* | / | %) term | term
    term := (expression) | Identifier | StringConstant | IntConstant | keyConst | FloatConstant | list
    keyConst := true | false | Anything | Nothing
    list := [term (, term)*]
    ```

## Syntax Tree

The following provides the overall structure of what the abstract syntax tree looks like.

### Modules

```json
{
    "module": {
        "name": "Example",
        "importable": true,
        "depends": [
            "Hive.*"
        ],
        "types": {},
        "datatypes": {},
        "functions": []
    }
}
```

### Custom Types

```json
"type": {
    "name": "Example",
    "shadows": "Boolean"
}
```

### Custom Datatypes

```json
"datatype": {
    "name": "Example",
    "structures": [
        "( Example1 String Int )"
    ]
}
```

### Functions

```json
"function": {
    "name": "exampleFn",
    "signature": {},
    "docstring": "",
    "body": []
}
```


### Function Signature

```json
"signature": {
    "parameter_types": [
        "Example"
    ],
    "return": [
        "Example"
    ]
}
```

### Function Body
```json
"body": [
    {
        "params": [
            "example"
        ],
        "result": {}
    }
]
```

### Expression
```json
"expression": {
    "operative_expression": {
        "operation": null,
        "left": {},
        "right": {}
    }
}
```
All expressions with operators follow the same basic pattern as `operative_expression`, but use different keys:

- `boolean_expression`
- `equality_expression`
- `low_inequal_expression`
- `high_inequal_expression`
- `additive_expression`
- `multiplicative_expression`

The operation is then set in the `operation` key if there is an operation present.

If nothing is present on either side of the tree's children, `"Nothing"` is put in place of that particular child.

### Term

```json
{
    "identifier": "Example"
}
```

`identifier` can be replaced with the appropriate term type that matches the value of the type. See below for information on lists as pairs.

### List Pair
```json
"list_constant": {
    "head": {},
    "tail": {}
}
```

<!-- ### Standard Expressions

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

The declaration grammars handle defining type and datatype declarations.

| Grammar | Corresponding Tokens |
| ------- | -------------------- |
| typeDeclaration | `'type' Identifier '=' type` |
| datatypeDeclaration | `'datatype' Identifier '=' Identifier type (type)* ('or' (Identifier type (type)*)*)*` |

### Modules

The module grammar handles defining modules. If a file does _not_ contain a module, a new module should be created with a random name (example: `__ocls_719472658`).

| Grammar | Corresponding Tokens |
| ------- | -------------------- |
| module | `(importStatements)* ('module' Identifier 'where')? (function | typeDeclaration | datatypeDeclaration)*` |
| importStatements | `'import' Identifier (('only' | 'except') Identifier (',' Identifier)*)?` | -->