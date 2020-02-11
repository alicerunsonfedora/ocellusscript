# ![OcellusScript](logomark.svg)

A Haskell-inspired functional programming language

[![MPL](https://img.shields.io/github/license/alicerunsonfedora/ocellusscript)](LICENSE.txt) 
![Python](https://img.shields.io/badge/python-2.7+-blue.svg) 
![GitHub Status](https://github.com/alicerunsonfedora/ocellusscript/workflows/Tests/badge.svg)

OcellusScript is a functional programming language, originally designed to work hand-in-hand with the coding mini game from the Unscripted visual novel. OcellusScript heavily draws inspiration and syntax from languages like Haskell, Swift, JavaScript/ES5, and Python. OcellusScript aims to be an easy-to-use, type safe, and powerful language.

This repository contains the specifications and documentation for the OcellusScript programming language, as well as the source code for Efficacy, the compiler and interpreter for OcellusScript.

> ⚠️ Note: OcellusScript is still a work in progress and is not fully functional as a language yet.

## Quick Links

- [OcellusScript Documentation](mkdocs/language/index.md)
- [OcellusScript Language Specification](mkdocs/language/11-spec.md)
- [OcellusScript Support for VS Code](https://github.com/alicerunsonfedora/ocellusscript-vscode)

## Build Requirements for Efficacy

- Python 2.7 or 3.7+ (3.7+ recommended)
- Poetry project manager

To build Efficacy, clone this repository and then run `poetry install`, followed by `poetry publish`.

## Efficacy Usage

To run Efficacy, just run `efficacy` into the terminal. Running it without any command should open the interactive interpreter environment.

### Additional arguments

- `-i file.ocls`/`--input file.ocls`: The path to the source file to compile.
- `-o exec`/`--output exec`: The path to the newly-created executable after compiling.
- `-oT tokens.json`/`--output-tokens tokens.json`: The path to the newly-created JSON file containing all of the tokens parsed.
- `-v`/`--version`: Reports the version of the Efficacy package. 