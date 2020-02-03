#!/usr/bin/env python3
"""This module contains the tests for Efficacy."""
from efficacy import __VERSION, OSTokenizer

class TestError(Exception):
    """The base TestError case."""

def test_version():
    """Test that the package version matches."""
    if __VERSION != "0.1.0":
        raise TestError("Version number doesn't match manifest.")

def test_lexer_on_string():
    """Test that the lexer can tokenize a given string."""
    lexer = OSTokenizer()
    source = "example t = t > 6 ? t + 5 : t"

    tokens = lexer.tokenize(source)
    if not tokens:
        raise TestError("Expected a list of tokens bu received an empty list.")

    print(tokens)

def test_lexer_on_file():
    """Test that the lexer can tokenize an OcellusScript file."""
    lexer = OSTokenizer()
    source = ""
    with open("main.ocls", "r") as srcfile:
        source = srcfile.read()
    tokens = lexer.tokenize(source)
    if not tokens:
        raise TestError("Expected a list of tokens but received an empty list.")

if __name__ == "__main__":
    test_version()
    test_lexer_on_string()
