"""This module contains the parser tests for Efficacy.

The following test functions are provided to test that the parser
works as intended.
"""

#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from os import getcwd
from efficacy import OSParser

def test_parser_basic():
    """Test that the lexer parses a basic module correctly."""
    source = """
module Test where

example t = (t > 5) ? t : 8
    """

    myparse = OSParser(source)
    assert len(myparse.parse()) > 0

def test_parser_file():
    """Test that the lexer can parse an entire module file correctly."""
    with open(getcwd() + "/examples/VillainDatabase.ocls", 'r') as file:
        myparse = OSParser(file.read())

    assert len(myparse.parse()) > 0
