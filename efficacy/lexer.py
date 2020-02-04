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
from typing import NewType

Keyword = NewType('Keyword', str)

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
    identifier = "Identifier"
    keyword = "Keyword"
    string = "StringConstant"
    docstring = "DocstringConstant"
    comment = "Comment"
    symbol = "SymbolConstant"
    num_integer = "IntConstant"
    num_float = "FloatConstant"
    operator = "Operator"
    number = "NumConstant"

class OSTokenizer(object):
    """The tokenizing class for OcellusScript.

    The tokenizer is responsible for converting a stream of characters
    into OcellusScript tokens that can be used for parsing.
    """

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
        symbols = "<>,?[]()-=+*/%`\\!:"
        return char in symbols

    def is_operator(self, char):
        """Check whether a character is an operator.

        Args:
            char: The character to check.

        Returns: Boolean indicated whether the character is an operator.
        """
        operators = ["<", ">", "-", "+", "-", "*", "/", "%", "=", "and", "not", "or"]
        return char in operators

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
                            "type",
                            "datatype"]

        valid_keywords = valid_basic_types + valid_statements
        return word in valid_keywords

    def tokenize(self, script=""):
        """Generate a list of tokens from a given string.

        Args:
            script: The string to tokenize.

        Returns: A list containing tuples with the token's type (`OSTokenType`) and token.
        """

        # Generate an empty list of tokens and the sample token, as well as the current
        # state, current character, and the token type.
        tokens = []
        token = ""
        state = _OSTokenState.start
        char = ""
        token_type = None

        # Take the current string and convert it into a list of characters.
        source = list(script)

        # Iterate through every character in the source list.
        while source:

            # Grab the front of the source queue.
            char = source.pop(0)

            # If we're not in a token already, check if we can start a token.
            if state == _OSTokenState.start:

                # Mark the token as an identifier.
                if char in ascii_letters:
                    token_type = OSTokenType.identifier

                # Mark the token as a number.
                elif char in digits:
                    token_type = OSTokenType.number

                # Mark the token as a spcial type of symbol. Comments and docstrings
                # take precedence, then operators, then regular symbols.
                elif self.is_symbol(char):

                    if char == "#":
                        token_type = OSTokenType.comment
                    elif char == "`":
                        token_type = OSTokenType.docstring
                    elif self.is_operator(char):
                        token_type = OSTokenType.operator
                    else:
                        token_type = OSTokenType.symbol

                # If we have found a token type, mark that we will begin processing
                # the next few characters for the token and add the current character
                # to the token.
                if token_type:
                    state = _OSTokenState.in_id
                    token += char

            # If we're currently processing the token, check to see if the current character
            # will end our token.
            elif state == _OSTokenState.in_id:

                # If we're looking at an identifier and the character isn't a letter, terminate
                # here and "unread" the character.
                if token_type == OSTokenType.identifier and char not in ascii_letters:
                    state = _OSTokenState.end
                    source.insert(0, char)

                # If we're looking at a number and the character isn't a digit, terminate here
                # and "unread" the character.
                elif token_type == OSTokenType.number and char not in digits:
                    state = _OSTokenState.end
                    source.insert(0, char)

                elif token_type == OSTokenType.comment and char == "\n":
                    state = _OSTokenState.end
                    source.insert(0, char)

                elif token_type == OSTokenType.docstring and char == "`":
                    state = _OSTokenState.end
                    token += char

                elif token_type == OSTokenType.operator and not self.is_operator(char):
                    state = _OSTokenState.end
                    source.insert(0, char)

                # If we're looking at a symbol and the character isn't a symbol, terminate here
                # and "unread" the character.
                elif token_type == OSTokenType.symbol and not self.is_symbol(char):
                    state = _OSTokenState.end
                    source.insert(0, char)

                # Otherwise, regardless of the type, add the character to the token.
                else:
                    token += char

            # If we're at the end of processing a token, add a tuple containing the token's type
            # and the token itself before resetting for the next iteration.
            elif state == _OSTokenState.end:

                # If the token is a keyword, change the token's type.
                if token_type == OSTokenType.identifier and self.is_keyword(token):
                    token_type = OSTokenType.keyword

                tokens.append((token_type, token))
                token = ""
                token_type = None
                state = _OSTokenState.start

        # Finally, return the list of tokens.
        return tokens

    def __init__(self):
        """Initialize the tokenizer."""
