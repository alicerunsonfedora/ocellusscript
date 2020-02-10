# Modules and Main Execution

OcellusScript works on a file-based level and supports creating and importing modules that contain other functions and utilities. When an OcellusScript file is written, it is considered a module in and of itself when the `module` function is defined. The following example in the file **vill.ocls** shows how a module is written:

```ocellusscript
module VillainDatabase where

type Reform = Boolean
type Name = String

datatype KnownVillain = Villain Name Reform

knownVillains takes Nothing returns [KnownVillains]
knownVillains = [(Villain "Nightmare Moon" true),
                 (Villain "Discord" true),
                 (Villain "Tirek" false),
                 (Villain "Tempest Shadow" false),
                 (Villain "Starlight Glimmer" false),
                 (Villain "Chrysalis" false)]

knownByReform takes Nothing returns [KnownVillains]
knownByReform = filter
                    (lambda (Villain _ reform) -> reform)
                    knownVillains

inVillainDatabase takes String returns Boolean
inVillainDatabase name = member
                            name
                            (map (lambda (Villain name _ ) -> name) knownVillains)
```

**vill.ocls** is a typical OcellusScript file, but because the `module` function is defined at the top, all functions and types in this file are publicly accessible to other OcellusScript files by importing `VillainDatabase`. For example, another file called **chr.ocls** can make use of everything inside this module by using the `import` function:

```ocellusscript
import VillainDatabase

foundChrysalis takes Nothing returns Boolean
foundChrysalis = inVillainDatabase "Chrysalis"
```

## Specific imports

Importing the entire module may not be necessary and could cost performance. OcellusScript can handle this with specific imports. Again, with **chr.ocls**, we can manually import the `inVillainDatabase` function without importing everything else with the `only` statement:

```ocellusscript
import VillainDatabase only inVillainDatabase

foundChrysalis takes Nothing returns Boolean
foundChrysalis = inVillainDatabase "Chrysalis"
```

Likewise, `except` will import the entire module except a specific function:

```ocellusscript
import VillainDatabase except knownByReform

foundChrysalis takes Nothing returns Boolean
foundChrysalis = inVillainDatabase "Chrysalis"
```

## Private functions

Modules expose every function and type in a file and make it publicly accessible, which may not be desired. To mitigate this, adding the keyword `private` in front of a function definition will make sure that the function does _not_ get imported when the module is imported.

Looking back at **vill.ocls**, we could probably make the `knownVillains` function private so, say, a villain can't delete their entry from the database:

```ocellusscript
module VillainDatabase where

type Reform = Boolean
type Name = String

datatype KnownVillain = Villain Name Reform

knownVillains takes Nothing returns [KnownVillains]
private knownVillains = [(Villain "Nightmare Moon" true),
                 (Villain "Discord" true),
                 (Villain "Tirek" false),
                 (Villain "Tempest Shadow" false),
                 (Villain "Starlight Glimmer" false),
                 (Villain "Chrysalis" false)]

knownByReform takes Nothing returns [KnownVillains]
knownByReform = filter
                    (lambda (Villain _ reform) -> reform)
                    knownVillains

inVillainDatabase takes String returns Boolean
inVillainDatabase name = member
                            name
                            (map (lambda (Villain name _ ) -> name) knownVillains)
```

Note that the `private` keyword does _not_ need to be in the type signature of the function.

## Documentation Strings and Comments

It's good practice to include documentation with your source code. Documentation often provides information on what a function will do or what a module contains. Documentation strings (docstrings) are denoted with a set of backticks (`\``) can be inserted between a type signature and a function definition like below:

```ocellusscript
inVillainDatabase takes String returns Boolean
`Check whether a villain is in the known villain database.

Arguments:
    name: The name of the person to search for.
`
inVillainDatabase name = member
                            name
                            (map (lambda (Villain name _ ) -> name) knownVillains)
```

If you want to write comments or notes in a file, you can use a single hash (`#`) and then keep typing. OcellusScript will not execute any code in triple-quotes or after a hash. Comments with a hash extend until the next line in a file.

To access documentation for a function, the `help` function can be called:

```ocellusscript
help inVillainDatabase
```

Where `help` accepts a single parameter, the callable function with a docstring. If no documentation is found, nothing is returned.

## Executing a File

Thus far, we've defined functions in OcellusScript but haven't quite interacted with them. There are two ways to interact with them:

- Importing the module into an interactive interpreter environment
- Defining a `main` function that will be executed when running a compiled version of a script

OcellusScript supports the `main` function to write a function that executes when you call on a file's executable:

```ocellusscript
import VillainDatabase

main args = log (inVillainDatabase "Twilight")
```

When the file above is run after compiling, the `main` function will be executed. The following is the type signature of the `main` function:

```ocellusscript
main takes [String?] returns Anything?
```

When the file is executed, it can take in parameters from the command line as parameters to `main`.