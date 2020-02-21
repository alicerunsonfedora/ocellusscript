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

    The parser is responsible for reading a list of tokens and converting the them into a
    traversable abstract syntax tree that can be used to compile into a program with LLVM or can
    be processed differently with a Python script.
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

    def parse(self):
        """Parse the list of tokens and return an abstract syntax tree.

        Returns: A JSON-like dictionary containing all of the parsed functions, expressions,
        and modules.

        Raises: OSParserError if there's an error in the syntax of the current token being
        processed.
        """
        self.__tree = self._parse_module()
        return self.__tree

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

    def _lookahead(self):
        """Perform a lookahead on the list of tokens without popping it off the stack."""
        if self._has_more_tokens():
            return self.__tokens[0]
        return None

    def _parse_module(self):
        """Create an OcellusScript module with a name, import statements, datatypes and custom
        types, and its functions.

        Returns: A JSON-like dictionary containing the data for the module.
        """
        module_name = "__ocls_" + str(randint(1, 999999999)).rjust(9, '0')
        importable = False
        imports = []
        types = []
        datatypes = []
        functions = []

        ctype, ctoken = self.__current_token
        if ctype == OSTokenType.keyword:
            if ctoken == "import":
                while ctoken == "import":
                    i_name = ""

                    ctype, ctoken = self._advance_token()
                    if ctype != OSTokenType.identifier:
                        raise OSParserError("Expected identifier in import statement: " % (ctoken))
                    i_name = ctoken

                    ctype, ctoken = self._advance_token()
                    if ctype == OSTokenType.keyword and ctoken in ["only", "except"]:
                        if ctoken == "only":
                            only = []
                            ctype, ctoken = self._advance_token()
                            if ctype != OSTokenType.identifier:
                                raise OSParserError("Expected identifier in selective import: %s"
                                                    % (ctoken))
                            only.append(ctoken)

                            ctype, ctoken = self._advance_token()

                            while ctype == OSTokenType.symbol and ctoken == ",":
                                ctype, ctoken = self._advance_token()
                                if ctype != OSTokenType.identifier:
                                    raise OSParserError("Expected identifier in \
                                                        selective import: %s"
                                                        % (ctoken))
                                only.append(ctoken)
                                ctype, ctoken = self._advance_token()

                            imports += map(lambda a: "%s.%s" % (i_name, a), only)
                        elif ctoken == "except":
                            exceptions = []
                            ctype, ctoken = self._advance_token()
                            if ctype != OSTokenType.identifier:
                                raise OSParserError("Expected identifier in \
                                                    selective import: %s"
                                                    % (ctoken))
                            exceptions.append(ctoken)

                            ctype, ctoken = self._advance_token()

                            while ctype == OSTokenType.symbol and ctoken == ",":
                                ctype, ctoken = self._advance_token()
                                if ctype != OSTokenType.identifier:
                                    raise OSParserError("Expected identifier in \
                                                        selective import: %s"
                                                        % (ctoken))
                                exceptions.append(ctoken)
                                self._advance_token()

                            imports += map(lambda a: "%s!%s" % (i_name, a), exceptions)
                    else:
                        imports += [i_name + ".*"]

            if ctoken == "module":
                ctype, ctoken = self._advance_token()

                if ctype != OSTokenType.identifier:
                    raise OSParserError("Expected identifier in module definition: %s"
                                        % (ctoken))

                module_name = ctoken
                importable = True
                ctype, ctoken = self._advance_token()

                if ctoken != "where" and ctype != OSTokenType.keyword:
                    raise OSParserError("Expected where keyword here: %s" % (ctoken))
                ctype, ctoken = self._advance_token()

        while ctype in [OSTokenType.identifier, OSTokenType.keyword]:
            if ctype == OSTokenType.keyword:
                if ctoken == "type":
                    types.append(self._parse_custom_type())
                elif ctoken == "datatype":
                    datatypes.append(self._parse_custom_datatype())
                else:
                    raise OSParserError("Unexpected keyword here: %s" % (ctoken))
            else:
                functions.append(self._parse_function())

        return {
            "module": {
                "name": module_name,
                "importable": importable,
                "depends": imports,
                "types": types,
                "datatypes": datatypes,
                "functions": functions
            }
        }

    def _parse_custom_type(self):
        raise NotImplementedError

    def _parse_custom_datatype(self):
        raise NotImplementedError

    def _parse_function(self):
        function_name = ""
        function_signature = {}
        function_docstring = ""
        function_body = {}

        ctype, ctoken = self.__current_token
        function_name = ctoken

        ltype, ltoken = self._lookahead()
        if ltype == OSTokenType.keyword and ltoken == "takes":
            function_signature = self._parse_signature()

        ctype, ctoken = self._advance_token()

        if ctype == OSTokenType.docstring:
            function_docstring = ctoken
            ctype, ctoken = self._advance_token()

        function_body = self._parse_function_body()

        return {
            "function": {
                "name": function_name,
                "signature": function_signature,
                "docstring": function_docstring,
                "body": function_body
            }
        }

    def _parse_signature(self):
        raise NotImplementedError

    def _parse_function_body(self):
        raise NotImplementedError

if __name__ == "__main__":
    EXAMPLE = """
import Hyperion except JackShit
import Ocellus only map
import Equestria

module NoJackShitHere where

square square = square * square"""
    print(OSParser(script=EXAMPLE).parse())
