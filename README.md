# OcellusScript

A Haskell-inspired functional programming language

[![MPL](https://img.shields.io/github/license/alicerunsonfedora/ocellusscript)](LICENSE.txt) 
![Python](https://img.shields.io/badge/python-2.7+-blue.svg) 
![GitHub Status](https://github.com/alicerunsonfedora/ocellusscript/workflows/Tests/badge.svg)

OcellusScript is a functional programming language designed to work hand-in-hand with Unscripted's minigame. It heavily draws inspiration from languages like Haskell, Swift, JavaScript/ES5, and Python. OcellusScript aims to be an easy-to-use language that can perform powerful tasks and includes features like pattern matching, optional types, ternary operators, custom data types, and documentation string.

This repository contains the specifications and documentation for the OcellusScript programming language, as well as the source code for Efficacy, the compiler and interpreter for OcellusScript.

> ⚠️ Note: OcellusScript is still a work in progress and is not fully functional as a language yet.

## Quick Links

- [OcellusScript Documentation](doc.md)
- [OcellusScript Technical Specifications](spec.md)

## Build Requirements for Efficacy

- Python 2.7 or 3.7+ (3.7+ recommended)
- Poetry project manager

To build Efficacy, clone this repository and then run `poetry install`, followed by `poetry publish`.