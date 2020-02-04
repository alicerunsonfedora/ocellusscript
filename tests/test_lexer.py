#!/usr/bin/env python3
"""This module contains the lexer tests for Efficacy.

The following test functions are provided to test that the lexer
works as intended for both files and regular strings.
"""
from efficacy import __VERSION, OSTokenizer
from tests.utils import test, TestError

@test
def test_lexer_on_string():
    """Test that the lexer can tokenize a given string."""
    lexer = OSTokenizer()
    source = "example t = t > 6 ? t + 5 : t"

    tokens = lexer.tokenize(source)
    if not tokens:
        raise TestError("Expected a list of tokens but received an empty list.")

    print(tokens)

@test
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
    print("Running lexer tests...")
    test_lexer_on_string()
    test_lexer_on_file()
