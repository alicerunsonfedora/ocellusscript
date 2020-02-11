"""
The `parser` submodule of Efficacy contains all of the tools necessary
to parse a list of tokens into an abstract syntax tree to be used for
compilation or additional processing.
"""

#
# OcellusScript Parser
# (C) 2020 Marquis Kurt.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

class OSParser(object):
    """The parsing class for OcellusScript.

    The parser is responsible for reading a list of tokens and converting
    the them into a traversable abstract syntax treee that can be used to
    compile into a program with LLVM or can be processed differently with
    a Python script.
    """
