"""
The `lexer` submodule of Efficacy contains all of the tools necessary
to tokenize a string or a file into a a list of OcellusScript tokens.
"""

#
# OcellusScript Tokenizer
# (C) 2020 Marquis Kurt.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from string import ascii_letters, digits
from enum import Enum

class OSTokenizerError(Exception):
    """An error used to indicate that the tokenizer has failed in some way."""

class _OSTokenState(Enum):
    """An enumeration type for the different token states.

    This enumeration is used internally to denote what state the
    tokenization process is in when processing a token and should
    not be used in other places.
    """
    start = "START"
    in_id = "IN PROGRESS"
    end = "FINISH"
    error = "ERRORED"

class OSTokenType(Enum):
    """An enumeration type for the different token types.

    This enumeration class is used to differentiate between
    the different types of tokens used for OcellusScript
    parsing. The values of the enumerations correspond to the
    lexical grammar names for each type.
    """
    keyword = "Keyword"
    identifier = "Identifier"
    string = "StringConstant"
    docstring = "DocstringConstant"
    comment = "CommentConstant"
    symbol = "Symbol"
    num_integer = "IntConstant"
    num_float = "FloatConstant"
    operator = "Operator"
    number = "NumConstant"

class OSTokenizer(object):
    """The tokenizing class for OcellusScript.

    The tokenizer is responsible for converting a stream of characters
    into OcellusScript tokens that can be used for parsing.
    """

    source = []

    def _contains_more_tokens(self):
        """Return whether the source isn't empty."""
        return len(self.source) > 0

    def _unread(self, item):
        """Insert the item to the front of the source queue.
        
        Args:
            item: The item to insert.
        """
        self.source.insert(0, item)

    def _get_next_char(self):
        """Returns the front of the source queue if it isn't empty."""
        if self._contains_more_tokens():
            return self.source.pop(0)

    def is_alpha_num(self, char):
        """Check whether a characer is an alphanumeric character.

        Args:
            char: The character to check against.

        Returns: Boolean indicating whether the character is alphanumeric.
        """
        return char in ascii_letters or char in digits

    def is_symbol(self, char):
        """Check whether a character is a symbol.

        Args:
            char: The character to check.

        Returns: Boolean indicating whether the character is a symbol.
        """
        symbols = "<>,?[]()-=+*/%`\\!:#_"
        return char in symbols

    def is_operator(self, partial):
        """Check whether a string is an operator.

        Args:
            partial: The string to check.

        Returns: Boolean indicated whether the character is an operator.
        """
        operators = ["<", ">", "-", "+", "-", "*", "/", "%",
                     "=", ">=", "<=", "==", "and", "not", "or", "??"]

        return partial in operators

    def is_keyword(self, word):
        """Determine whether the list of characters corresponds to
        a keyword.

        Args:
            word: The string to check.
        """
        valid_basic_types = ["Character",
                             "String",
                             "Integer",
                             "Boolean",
                             "Float",
                             "Callable",
                             "Anything",
                             "Nothing",
                             "Error"]

        valid_statements = ["import",
                            "module",
                            "where",
                            "takes",
                            "returns",
                            "log",
                            "only",
                            "except",
                            "warn",
                            "true",
                            "false",
                            "type",
                            "datatype",
                            "private"]

        valid_keywords = valid_basic_types + valid_statements
        return word in valid_keywords

    def _get_token(self):
        """Generate a single token from the source list.

        Returns a tuple containing the token's type and the token itself.
        """
        token = char = ""
        state = _OSTokenState.start
        token_type = None

        while (state != _OSTokenState.end and state != _OSTokenState.error):
            if not self._contains_more_tokens():
                break

            char = self._get_next_char()

            if state == _OSTokenState.start:
                if char in ascii_letters:
                    token_type = OSTokenType.identifier
                elif char in digits:
                    token_type = OSTokenType.number
                elif char == "\"":
                    token_type = OSTokenType.string
                elif char == "#":
                    token_type = OSTokenType.comment
                elif char == "`":
                    token_type = OSTokenType.docstring
                elif self.is_symbol(char):
                    token_type = OSTokenType.symbol
                else:
                    continue

                if token_type is not None:
                    state = _OSTokenState.in_id
                    if token_type != OSTokenType.string:
                        token += char

            elif state == _OSTokenState.in_id:
                if token_type == OSTokenType.identifier:
                    if char not in ascii_letters:
                        state = _OSTokenState.end
                        self._unread(char)
                    else:
                        token += char
                elif token_type == OSTokenType.number:
                    if char == ".":
                        token_type = OSTokenType.num_float
                        token += char
                    else:
                        if char not in digits:
                            token_type = OSTokenType.num_integer
                            state = _OSTokenState.end
                            self._unread(char)
                        else:
                            token += char
                elif token_type == OSTokenType.num_float:
                    if char not in digits:
                        state = _OSTokenState.end
                        self._unread(char)
                    else:
                        token += char
                elif token_type == OSTokenType.string:
                    if char == "\"":
                        state = _OSTokenState.end
                    else:
                        token += char
                elif token_type == OSTokenType.comment:
                    if char == "\n":
                        state = _OSTokenState.end
                        self._unread(char)
                    else:
                        token += char
                elif token_type == OSTokenType.docstring:
                    if char == "`":
                        state = _OSTokenState.end
                    else:
                        token += char
                elif token_type == OSTokenType.symbol:
                    state = _OSTokenState.end
                    self._unread(char)

        if state == _OSTokenState.error:
            raise OSTokenizerError("Tokenizing failed.")

        if token_type == OSTokenType.identifier and self.is_keyword(token):
            token_type = OSTokenType.keyword

        return token_type, token

    def tokenize(self):
        """Generate a list of tokens from a given string.

        Args:
            script: The string to tokenize.

        Returns: A list containing the tokens as a tuple containing the token's type and
        the token itself.
        """

        # Generate an empty list of tokens and the sample token, as well as the current
        # state, current character, and the token type.
        tokens = []

        # Generate the tokens while the source isn't empty.
        while self._contains_more_tokens():
            t = self._get_token()
            if t[0] != OSTokenType.comment:
                tokens.append(t)

        # Finally, return the list of tokens.
        return tokens

    def __init__(self, script=""):
        """Initialize the tokenizer."""
        self.source = list(script)
