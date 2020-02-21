"""
The `parser` submodule of Efficacy contains all of the tools necessary
to parse a list of tokens into an abstract syntax tree to be used for
compilation or additional processing.
"""

#
# OcellusScript Parser (Reborn)
# (C) 2020 Marquis Kurt.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from random import randint
from efficacy.lexer import OSTokenType, OSTokenizer

class OSParserError(Exception):
    """The base error to use when the parser has failed."""

class OSParser(object):
    """The parsing class for OcellusScript.

    The parser is responsible for reading a list of tokens and converting
    the them into a traversable abstract syntax treee that can be used to
    compile into a program with LLVM or can be processed differently with
    a Python script.
    """
    _tokenizer = OSTokenizer("")
    __current_token = None, None
    __tokens = []
    __tree = {}

    def __init__(self, **kwargs):
        """Initialize the OcellusScript Parser object.

        Keyword Args:
            script: The string containing the code to parse. The parser will tokenize this
            script before parsing it.
            tokens: The pre-processed list of tokens to use for parsing.
        """
        if 'script' in kwargs.keys():
            self._tokenizer = OSTokenizer(kwargs['script'])
            self.__tokens = self._tokenizer.tokenize()
        elif 'tokens' in kwargs.keys():
            self.__tokens = kwargs['tokens']
        else:
            raise TypeError("OSParser expects either 'script' or 'tokens' to be defined.")

        self.__tree = {}
        self.__current_token = self._advance_token()

    def _has_more_tokens(self):
        """Return whether the parser's token list has more tokens."""
        return len(self.__tokens) > 0

    def _advance_token(self):
        """Get the next available token.

        Dequeues the first token from the tokens list and returns it if there are more tokens.
        Otherwise, this will return None.
        """
        if self._has_more_tokens():
            self.__current_token = self.__tokens.pop(0)
            return self.__current_token
        return None
