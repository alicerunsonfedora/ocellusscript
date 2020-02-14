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

from random import random
from efficacy.lexer import OSTokenizer, OSTokenType
from efficacy.ast import * # pylint: disable=wildcard-import

class OSParserError(Exception):
    """The error to use when the parser has failed."""

class OSParser(object):
    """The parsing class for OcellusScript.

    The parser is responsible for reading a list of tokens and converting
    the them into a traversable abstract syntax treee that can be used to
    compile into a program with LLVM or can be processed differently with
    a Python script.
    """

    _tokenizer = OSTokenizer("")
    _tokens = []
    _tree = []

    __previous = None, None
    __current = None, None
    __newtypes = []
    __newfuncs = []

    def _advance(self):
        """If there are more tokens available, store the current token as
        the previous token (n - 1) and fetch the next token to be stored
        as the current one."""
        if len(self._tokens) > 0:
            self.__previous = self.__current
            self.__current = self._tokens.pop(0)

    def _revert(self):
        """Roll back the most recent action and push it back into the list
        of tokens.

        Always sets `__previous` to `None`, `None`, regardless of the previous
        values in that list.
        """
        if self.__previous != (None, None):
            self._tokens.insert(0, self.__previous)
            self.__current = self.__previous
            self.__previous = None, None

    def _keyword_constant(self, keyword):
        """Get an appropriate keyword constant node, if available.

        Returns: A subclassed `OSTypeNode` depending on the keyword
        in question. Booleans return the `OSBooleanTypeNode` type,
        while Anything and Nothing return their respective type
        nodes.

        Raises: Raises an `OSParserError` if the keyword is not a valid
        keyword constant.
        """
        if keyword not in ["true", "false", "Anything", "Nothing"]:
            raise OSParserError("%s is not a valid keyword constant." % (keyword))

        if keyword == "true" or keyword == "false":
            return OSBooleanTypeNode(value=keyword)
        elif keyword == "Anything":
            return OSAnythingTypeNode(value=None)
        else:
            return OSNothingTypeNode()

    def _basic_expression(self):
        """Get a basic expression, if available.

        Basic expressions are considered standard, single primitive types
        (`"I at the dog."`) or an expression wrapped in a set of parentheses
        (`(2 + 8)`).

        Returns: A subclassed `OSTypeNode`, or an `OSExpressionNode` if
        the expression is parenthetical and contains additional operations
        inside.

        Raises: `OSParserError` if the expression in question is not valid.
        """
        ctype, ctoken = self.__current
        if ctype == OSTokenType.string:
            return OSStringTypeNode(value=ctoken)
        elif ctype == OSTokenType.num_integer:
            return OSIntTypeNode(value=ctoken)
        elif ctype == OSTokenType.num_float:
            return OSFloatTypeNode(value=ctoken)
        elif ctype == OSTokenType.keyword:
            return self._keyword_constant(ctoken)
        elif ctype == OSTokenType.symbol and ctoken == "(":
            return self._expression()
        else:
            raise OSParserError("%s is not a valid expression in this context." % (ctoken))

    def _multiplicative_expression(self):
        ctype, ctoken = self.__current
        raise NotImplementedError()

    def _additive_expression(self):
        raise NotImplementedError()

    def _valued_expression(self):
        raise NotImplementedError()

    def _inequality_expression(self):
        raise NotImplementedError()

    def _equality_expression(self):
        raise NotImplementedError()

    def _boolean_expression(self):
        raise NotImplementedError()

    def _expression(self):
        raise NotImplementedError()

    def _type(self):
        """Get a type, if available.

        Returns: Either an `OSOptionalTypeNode` for an optional type
        or an `OSTypeNode` containing the type in question.

        Raises: `OSParserError` if the type passed was not a primitive
        type or a type that was previously defined before.
        """
        ctype, ctoken = self.__current
        standard_types = ["String", "Integer", "Character", "Float",
                          "Boolean", "Anything", "Nothing", "Callable"]
        if ctype != OSTokenType.identifier and ctype != OSTokenType.keyword:
            raise OSParserError("Expected an identifier or keyword here: %s" % ctoken)
        if ctoken not in standard_types and ctoken not in self.__newtypes:
            raise OSParserError("%s is not a valid type." % ctoken)

        typename = ctoken

        self._advance()
        ctype, ctoken = self.__current

        if ctype == OSTokenType.symbol and ctoken == "?":
            return OSOptionalTypeNode(possible_value=None, possible_type=ctype)
        else:
            return OSTypeNode(typename, typevalue=None)

    def _type_list(self):
        """Get a list of types, if available.

        Returns: A list of `OSOptionalTypeNode` and/or `OSTypeNode`.

        Raises: `OSParser` error if any type in the list is not a primitive
        type or a custom-defined type.
        """
        ctype, ctoken = self.__current
        if ctype != OSTokenType.keyword and ctype != OSTokenType.identifier:
            raise OSParserError("%s is not a valid keyword or identifier." % (ctoken))

        types = [self._type()]
        self._advance()
        ctype, ctoken = self.__current

        while ctype == OSTokenType.keyword and ctoken == "and":
            self._advance()
            types.append(self._type())
            self._advance()

        return types

    def _fn_signature(self):
        """Get a function type signature, if available.

        Returns: `OSSignatureNode` containing the signature properties of the
        function.

        Raises: `OSParserError` if the signature is invalid.
        """
        ctype, ctoken = self.__current
        if ctoken in self.__newfuncs:
            raise OSParserError("Type signature for %s already defined." % (ctoken))

        fn_name = ctoken
        input_types = None
        output_type = None

        self._advance()
        ctype, ctoken = self.__current

        if ctype != OSTokenType.keyword and ctoken != "takes":
            raise OSParserError("Expected 'takes' here in type signature but got %s instead."
                                % (ctoken))

        self._advance()
        input_types = self._type_list()

        if ctype != OSTokenType.keyword and ctoken != "returns":
            raise OSParserError("Expected 'returns' here in type signature but got %s instead."
                                % (ctoken))
        self._advance()
        output_type = self._type()

        return OSSignatureNode(name=fn_name, input=input_types, output=output_type)

    def _fn_return(self):
        """Get the function call return statement, if available.

        Returns: `OSFunctionReturnNode` containing the function name and the
        paramaters passed, as well as any inline function calls.

        Raises: `OSParserError` if the function call return is invalid.
        """
        ctype, ctoken = self.__current
        if ctype != OSTokenType.identifier:
            raise OSParserError("Expected an identifier, received %s instead."
                                % (ctoken))

        fn_name = ctoken
        fn_params = []
        fn_definition = None
        self._advance()
        ctype, ctoken = self.__current

        if ctype == OSTokenType.identifier:
            while ctype == OSTokenType.identifier:
                fn_params.append(ctoken)
                self._advance()
                ctype, ctoken = self.__current

        if ctype == OSTokenType.keyword and ctoken == "where":
            self._advance()
            fn_definition = self._fn_definition()

        return OSFunctionReturnNode(name=fn_name,
                                    params=fn_params,
                                    defines_inline=fn_definition is not None,
                                    inline_func=fn_definition)


    def _fn_definition(self):
        """Get a function definition, if available.

        Returns: `OSFunctionNode` with a child expression tree, optional signature,
        and docstring.

        Raises: `OSParserError` if the function definition is invalid.
        """
        ctype, ctoken = self.__current

        fn_private = False

        if ctype == OSTokenType.keyword and ctoken == "private":
            fn_private = True
            self._advance()
            ctype, ctoken = self.__current

        if ctype != OSTokenType.identifier:
            raise OSParserError("Expected a function identifier here: %s" % (ctoken))

        fn_name = ctoken
        fn_signature = None
        fn_docstring = None
        fn_result = None
        fn_params = []

        if fn_name in self.__newfuncs:
            raise OSParserError("Function %s was already defined." % (fn_name))

        self._advance()
        ntype, _ = self.__current
        if ntype == OSTokenType.keyword:
            self._revert()
            fn_signature = self._fn_signature()
            self._advance()

        ctype, ctoken = self.__current
        if ctype == OSTokenType.docstring:
            fn_docstring = ctoken

        self._advance()
        ctype, ctoken = self.__current

        if ctype == OSTokenType.identifier:
            while ctype == OSTokenType.identifier:
                fn_params.append(ctoken)
                self._advance()
                ctype, ctoken = self.__current
        else:
            fn_params = [OSNothingTypeNode()]

        self._advance()
        ctype, ctoken = self.__current
        if ctype != OSTokenType.symbol and ctoken != "=":
            raise OSParserError("Expected assignment in function definition, got %s instead."
                                % (ctoken))

        self._advance()
        ctype, ctoken = self.__current

        fn_result = self._expression()

        self.__newfuncs.append(fn_name)

        return OSFunctionNode(name=fn_name,
                              result=fn_result,
                              signature=fn_signature,
                              docstring=fn_docstring,
                              private=fn_private)

    def _type_declaration(self):
        raise NotImplementedError()

    def _datatype_declaration(self):
        raise NotImplementedError()

    def _imports(self):
        """Get all import statements, if possible.

        Returns: A list of strings containing what to import.

        Raises: `OSParserError` if import parsing fails.
        """
        depends = []
        import_name = ""
        ctype, ctoken = self.__current

        while ctype == OSTokenType.keyword and ctoken == "import":
            self._advance()
            ctype, ctoken = self.__current
            if ctype != OSTokenType.identifier:
                raise OSParserError("Expected a module identifier here but got %s instead"
                                    % (ctoken))
            import_name = ctoken
            self._advance()
            ctype, ctoken = self.__current

            if ctype == OSTokenType.keyword:
                if ctoken == "except":
                    no_imports = []
                    self._advance()
                    ctype, ctoken = self.__current

                    if ctype != OSTokenType.identifier:
                        raise OSParserError("Expected a function identifier\
                                                here but got %s instead"
                                            % (ctoken))

                    while ctype == OSTokenType.identifier:
                        no_imports.append(ctoken)
                        self._advance()

                        ctype, ctoken = self.__current

                        while ctype == OSTokenType.symbol and ctoken == ",":
                            self._advance()
                            ctype, ctoken = self.__current
                            no_imports.append(ctoken)
                            self._advance()

                    no_imports = list(map(lambda a: import_name + "!" + a, no_imports))
                    depends += no_imports
                elif ctoken == "only":
                    only_imports = []
                    self._advance()
                    ctype, ctoken = self.__current

                    if ctype != OSTokenType.identifier:
                        raise OSParserError("Expected a function identifier\
                                                here but got %s instead"
                                            % (ctoken))

                    while ctype == OSTokenType.identifier:
                        only_imports.append(ctoken)
                        self._advance()

                        ctype, ctoken = self.__current

                        while ctype == OSTokenType.symbol and ctoken == ",":
                            self._advance()
                            ctype, ctoken = self.__current
                            only_imports.append(ctoken)
                            self._advance()

                    no_imports = list(map(lambda a: import_name + "." + a, only_imports))
                    depends += only_imports
                else:
                    raise OSParserError("Unexpected keyword %s in import statement" % (ctoken))
        return depends

    def _md_definition(self):
        """Get a module definition.

        Returns: `OSModuleNode` with the dependencies and child functions/types defined. If no name
        was detected, a random name similar to the following is assigned instead:
        `ocellus_173646287183`.

        Raises: `OSParserError` if parsing the module failed.
        """
        ctype, ctoken = self.__current
        name = ""
        dependencies = []
        fns = []

        if ctype == OSTokenType.keyword and ctoken == "import":
            dependencies = self._imports()
            self._advance()
            ctype, ctoken = self.__current

        if ctype != OSTokenType.keyword and ctoken != "module":
            name = "ocellus_" + str(random())
        else:
            self._advance()
            ctype, ctoken = self.__current
            if ctype != OSTokenType.identifier:
                raise OSParserError("Expected module name identifier but got %s instead"
                                    % (ctoken))
            name = ctoken

        self._advance()
        ctype, ctoken = self.__current
        if ctype != OSTokenType.keyword and ctoken != "where":
            raise OSParserError("Expected where keyword here but got %s instead." % (ctoken))

        self._advance()
        ctype, ctoken = self.__current

        while ctype == OSTokenType.identifier or ctype == OSTokenType.keyword:
            if ctype == OSTokenType.keyword:
                if ctoken == "type":
                    fns.append(self._type_declaration())
                elif ctoken == "datatype":
                    fns.append(self._datatype_declaration())
                else:
                    raise OSParserError("Unexpected keyword %s found here." % (ctoken))
            else:
                fns.append(self._fn_definition())

            self._advance()
            ctype, ctoken = self.__current

        return OSModuleNode(name, fns, dependencies=dependencies)

    def parse(self):
        """Parse through the list of tokens or script and return the expression
        tree, if there are no errors.

        If an error occurs during the parsing processing, the parser throws an
        `OSParserError`.

        Returns: A list containing the abstract syntax tree of the OcellusScript
        code.

        Raises: `OSParserError` if any part of the parsing fails.
        """
        if not self._tokens and self._tokenizer.source:
            self._tokens = self._tokenizer.tokenize()
        self._advance()
        self._tree = [self._md_definition()]
        return self._tree

    def __init__(self, script="", tokens=None):
        """Construct the parser object.

        When constructing this object, either a script that can be tokenized
        can be passed or a list of existing tokens.

        Arguments:
            script: The script to tokenize and then parse.
            tokens: A pre-existing list tokens to parse.

        Raises: `OSParserError` if both a script and a list of tokens are provided.
        """
        self._tokenizer = OSTokenizer(script)

        if tokens:
            if script:
                raise OSParserError("Cannot instantiate parser with both a script and list of tokens.")
            self._tokens = tokens

        self._tree = []
        self.__current = self.__previous = None, None
        self.__newtypes = self.__newfuncs = []
