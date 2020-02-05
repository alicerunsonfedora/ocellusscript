"""This module contains the lexer tests for Efficacy.

The following test functions are provided to test that the lexer
works as intended for both files and regular strings.
"""
from os import getcwd
from efficacy import OSTokenizer

def test_tokenize_basic_string():
    """Test that the lexer can tokenize a given string."""
    lexer = OSTokenizer()
    source = "example takes Integer returns Integer\nexample t = t > 6 ? t + 5 : t\n"

    tokens = lexer.tokenize(source)
    assert len(tokens) > 0

def test_tokenize_file():
    """Test that the lexer can tokenize an OcellusScript file."""
    lexer = OSTokenizer()
    source = ""
    with open(getcwd() + "/tests/main.ocls", "r") as srcfile:
        source = srcfile.read()
    tokens = lexer.tokenize(source)
    assert len(tokens) > 0
