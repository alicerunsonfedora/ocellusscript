"""This module contains the lexer tests for Efficacy.

The following test functions are provided to test that the lexer
works as intended for both files and regular strings.
"""

#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

import json
from os import getcwd
from efficacy import OSTokenizer

def test_tokenize_basic():
    """Test that the lexer can tokenize a basic string.

    This test will also attempt to verify that the tokens match what's
    processed in the lexer_samples folder.
    """
    lexer = OSTokenizer()
    source = "example t = t > 6.0 ? t + 5.3 : t\n"

    tokens = []
    expected_tokens = []
    all_tokens = lexer.tokenize(source)
    for token_type, token in all_tokens:
        token_key = token_type if isinstance(token_type, str) else token_type.value
        tokens.append({token_key: token})
    with open(getcwd() + "/tests/lexer_samples/basic.json", "r") as sample:
        expected_tokens = json.load(sample)
    assert tokens == expected_tokens

def test_tokenize_basic_with_docstring():
    """Test that the lexer can tokenize a basic string with a docstring.

    This test will also attempt to verify that the tokens match what's
    processed in the lexer_samples folder.
    """
    lexer = OSTokenizer()
    source = "example takes Float returns Float\n" \
             + "`Add 5.3 to a value if it's greater than 6.`\n" \
             + "example t = t > 6.0 ? t + 5.3 : t\n"

    tokens = []
    expected_tokens = []
    all_tokens = lexer.tokenize(source)
    for token_type, token in all_tokens:
        token_key = token_type if isinstance(token_type, str) else token_type.value
        tokens.append({token_key: token})
    with open(getcwd() + "/tests/lexer_samples/basic_with_docstring.json", "r") as sample:
        expected_tokens = json.load(sample)
    assert tokens == expected_tokens

def test_tokenize_file():
    """Test that the lexer can tokenize an OcellusScript file."""
    lexer = OSTokenizer()
    source = ""
    with open(getcwd() + "/tests/main.ocls", "r") as srcfile:
        source = srcfile.read()
    tokens = lexer.tokenize(source)
    assert len(tokens) > 0
