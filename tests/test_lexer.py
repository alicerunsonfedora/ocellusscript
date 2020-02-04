#!/usr/bin/env python3
"""This module contains the lexer tests for Efficacy.

The following test functions are provided to test that the lexer
works as intended for both files and regular strings.
"""
from efficacy import OSTokenizer, OSTokenType
from tests.utils import test, TestError
from os import getcwd

@test(name="basic string tokenization")
def tokenize_basic_string():
    """Test that the lexer can tokenize a given string."""
    lexer = OSTokenizer()
    source = "example t = t > 6 ? t + 5 : t\n"

    tokens = lexer.tokenize(source)
    if not tokens:
        raise TestError("Expected a list of tokens but received an empty list.")

    expected = [(OSTokenType.identifier, 'example'),
                (OSTokenType.identifier, 't'),
                (OSTokenType.operator, '='),
                (OSTokenType.identifier, 't'),
                (OSTokenType.operator, '>'),
                (OSTokenType.number, '6'),
                (OSTokenType.symbol, '?'),
                (OSTokenType.identifier, 't'),
                (OSTokenType.operator, '+'),
                (OSTokenType.number, '5'),
                (OSTokenType.symbol, ':'),
                (OSTokenType.identifier, 't')]
    if tokens != expected:
        raise TestError("Tokenized list doesn't match expected tokens.")

@test(name="file tokenization")
def tokenize_file():
    """Test that the lexer can tokenize an OcellusScript file."""
    lexer = OSTokenizer()
    source = ""
    with open(getcwd() + "/tests/main.ocls", "r") as srcfile:
        source = srcfile.read()
    tokens = lexer.tokenize(source)
    if not tokens:
        raise TestError("Expected a list of tokens but received an empty list.")

if __name__ == "__main__":
    print("Running lexer tests...")
    tokenize_basic_string()
    tokenize_file()
