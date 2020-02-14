"""
Efficacy is a lexer, compiler, and interpreter for OcellusScript.

The `efficacy` module contains all of the publicly available tools
for Efficacy that include, but are not limited to:

- The tokenizer (`OSTokenizer`)
- The parser (`OSParser`)
- The compiler (`OSCompiler`)

This module also contains the interactive CLI program to convert
OcellusScript files to executable code.
"""

#
# OcellusScript Efficacy Module
# (C) 2020 Marquis Kurt.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from efficacy.lexer import *
from efficacy.parser import *
from efficacy.cli import run_cli

__VERSION = "0.1.0"

def main():
    """The main function."""
    run_cli()
