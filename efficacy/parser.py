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
from efficacy.ast import * # pylint: disable=wildcard-import,unused-wildcard-import

class OSParserError(Exception):
    """The error to use when the parser has failed."""

class OSSyntaxError(OSParserError):
    """The error to use when the parser has encountered a syntax error."""

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
    _standard_types = ["String", "Integer", "Character", "Float",
                       "Boolean", "Anything", "Nothing", "Callable"]

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
            self._tokens.insert(0, self.__current)
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

        if ctype == OSTokenType.num_integer:
            return OSIntTypeNode(value=ctoken)

        if ctype == OSTokenType.num_float:
            return OSFloatTypeNode(value=ctoken)

        if ctype == OSTokenType.keyword:
            return self._keyword_constant(ctoken)

        if ctype == OSTokenType.symbol and ctoken == "(":
            return self._expression()

        if ctype == OSTokenType.symbol and ctoken == "[":
            return self._list_expression()

        raise OSParserError("%s is not a valid expression in this context." % (ctoken))

    def _list_expression(self):
        ctype, ctoken = self.__current
        list_item_stack = []
        if ctype != OSTokenType.symbol and ctoken != "[":
            raise OSSyntaxError("Missing list opening bracket, got %s instead" % (ctoken))

        self._advance()
        ctype, ctoken = self.__current

        while ctoken != "]":
            self._advance()
            ctype, ctoken = self.__current
            list_item_stack.append(self._expression())
            # self._advance()

            while ctype == OSTokenType.symbol and ctoken == ",":
                self._advance()
                ctype, ctoken = self.__current
                list_item_stack.append(self._expression())

        self._advance()

        tree = OSListPairNode(head=list_item_stack.pop())

        while len(list_item_stack) > 0:
            item = list_item_stack.pop()
            tree = OSListPairNode(head=item, tail=tree)

        return tree

    def _multiplicative_expression(self):
        """Get a multiplicative expression node, if available.

        Returns: `OSExpressionNode` with the operator at the top, and the branches
        being the expressions to multiply, divide, or get the remainder of from division.
        If no operator was provided (i.e., the expression is not a multiplicative expression),
        `"expr"` will be used as the operator.

        Raises: `OSParserError` if the parsing of the expression failed.
        """
        lhs = rhs = None
        oper = "expr"
        ctype, ctoken = self.__current

        lhs = self._basic_expression()
        self._advance()
        ctype, ctoken = self.__current

        if ctype == OSTokenType.symbol:
            if ctoken not in ["*", "/", "%"]:
                raise OSSyntaxError("Expected multiplicative operator here: %s" % (ctoken))
            oper = ctoken
            self._advance()
            ctype, ctoken = self.__current
            rhs = self._basic_expression()

        return OSExpressionNode(oper, lhs, rhs)

    def _additive_expression(self):
        """Get an additive expression node, if available.

        Returns: `OSExpressionNode` with the operator at the top, and the branches
        being the expressions to add or subtract. If no operator was provided (i.e.,
        the expression is not an additive expression), `"expr"` will be used as the
        operator.

        Raises: `OSParserError` if the parsing of the expression failed.
        """
        lhs = rhs = None
        oper = "expr"
        ctype, ctoken = self.__current

        lhs = self._multiplicative_expression()
        self._advance()
        ctype, ctoken = self.__current

        if ctype == OSTokenType.symbol:
            if ctoken not in ["+", "-"]:
                raise OSSyntaxError("Expected additive operator here: %s" % (ctoken))

            oper = ctoken
            self._advance()
            ctype, ctoken = self.__current

            rhs = self._multiplicative_expression()

        return OSExpressionNode(oper, lhs, rhs)


    def _valued_expression(self):
        """Get a value expression node, if available.

        Value expressions refer to inequalities that do not compare equality directly
        (i.e., `>` and `<`).

        Returns: `OSExpressionNode` with the operator at the top, and the branches
        being the expressions to check for inequality. If no operator was provided (i.e.,
        the expression is not a value expression), `"expr"` will be used as the
        operator.

        Raises: `OSParserError` if the parsing of the expression failed.
        """
        lhs = rhs = None
        oper = "expr"
        ctype, ctoken = self.__current

        lhs = self._additive_expression()
        self._advance()
        ctype, ctoken = self.__current

        if ctype == OSTokenType.symbol:
            if ctoken not in [">", "<"]:
                raise OSSyntaxError("Expected value operator here: %s" % (ctoken))
            oper = ctoken
            self._advance()
            ctype, ctoken = self.__current

            rhs = self._additive_expression()

        return OSExpressionNode(oper, lhs, rhs)

    def _inequality_expression(self):
        """Get an inequality expression node, if available.

        Inequality expressions refer to inequalities such as `>=` and `<=`. Expressions
        without including a value are considered "value expressions". These expressions
        are separate from each other to indicate precedence of these types of expressions
        over exclusive inequalities.

        Returns: `OSExpressionNode` with the operator at the top, and the branches
        being the expressions to check for inequality. If no operator was provided (i.e.,
        the expression is not an inequality expression), `"expr"` will be used as the
        operator.

        Raises: `OSParserError` if the parsing of the expression failed.
        """
        lhs = rhs = None
        oper = "expr"
        ctype, ctoken = self.__current

        lhs = self._valued_expression()
        self._advance()
        ctype, ctoken = self.__current

        if ctype == OSTokenType.symbol:
            if ctoken not in [">", "<"]:
                raise OSSyntaxError("Expected inequality operator here: %s" % (ctoken))
            oper = ctoken
            self._advance()
            ctype, ctoken = self.__current

            if ctype != OSTokenType.symbol and ctoken != "=":
                raise OSSyntaxError("Expected inequality operator here: %s" % (ctoken))
            oper += ctoken
            self._advance()
            ctype, ctoken = self.__current

            rhs = self._valued_expression()

        return OSExpressionNode(oper, lhs, rhs)

    def _equality_expression(self):
        """Get an equality expression node, if available.

        Returns: `OSExpressionNode` with the operator at the top, and the branches
        being the expressions to check for equality. If no operator was provided (i.e.,
        the expression is not an equality expression), `"expr"` will be used as the
        operator.

        Raises: `OSParserError` if the parsing of the expression failed.
        """
        lhs = rhs = None
        oper = "expr"
        ctype, ctoken = self.__current

        lhs = self._inequality_expression()
        self._advance()
        ctype, ctoken = self.__current

        if ctype == OSTokenType.symbol:
            if ctoken not in ["=", "!"]:
                raise OSSyntaxError("Expected expression operator here: %s" % (ctoken))

            oper = ctoken
            self._advance()
            ctype, ctoken = self.__current
            if ctype != OSTokenType.symbol and ctoken != "=":
                raise OSSyntaxError("Expected expression operator here: %s" % (ctoken))

            oper += ctoken
            self._advance()
            ctype, ctoken = self.__current

            rhs = self._inequality_expression()

        return OSExpressionNode(oper, lhs, rhs)


    def _boolean_expression(self):
        """Get a boolean expression, if available.

        Returns: `OSExpressionNode` with the boolean operator at the root
        and the compared expressions as children (or None). If no operator was
        provided (i.e., the expression is not a boolean expression), `"expr"`
        will be used as the operator.

        Raises: `OSParserError` if the parsing of the expression failed.
        """
        lhs = rhs = None
        oper = "expr"
        ctype, ctoken = self.__current

        if ctype == OSTokenType.keyword and ctoken == "not":
            oper = ctoken
            self._advance()
            ctype, ctoken = self.__current

        lhs = self._equality_expression()
        self._advance()
        ctype, ctoken = self.__current

        if ctype == OSTokenType.keyword:
            if ctoken not in ["and", "or"]:
                raise OSParserError("Expected operation keyword but got %s instead" % (ctoken))

            oper = ctoken
            self._advance()
            ctype, ctoken = self.__current

            rhs = self._equality_expression()

        return OSExpressionNode(oper, lhs, rhs)

    def _expression(self):
        """Get an expression node, if available.

        An expression can either be the return call from a function, a conditional
        expression, an optional expression (`e ?? 0`), or a deeper boolean expression.

        Returns: `OSExpressionNode` if the expression is a deeper expression or optional
        expression, `OSFunctionReturnNode` if the expression if a function return call, or
        `OSConditionalExpressionNode` if the expression is a conditional expression.

        Raises: `OSParserError` if the parsing of the expression failed.
        """
        lhs = rhs = cond = None
        oper = "expr"
        ctype, ctoken = self.__current

        if ctype == OSTokenType.identifier:
            if ctoken in self.__newtypes:
                return self._datatype_options
            elif ctoken in self.__newfuncs:
                return self._fn_return()
            else:
                return OSFunctionVariableNode(ctoken)
        else:
            lhs = self._boolean_expression()

        self._advance()
        ctype, ctoken = self.__current

        if ctype == OSTokenType.symbol:
            if ctoken == "?":
                cond = lhs
                lhs = None
                self._advance()
                ctype, ctoken = self.__current

                if ctoken == OSTokenType.symbol and ctoken == "?":
                    oper = "??"
                    lhs = cond
                    cond = None
                    self._advance()
                    ctype, ctoken = self.__current
                    rhs = self._expression()

                    return OSExpressionNode(oper, lhs, rhs)

                lhs = self._expression()
                self._advance()
                ctype, ctoken = self.__current

                if ctype != OSTokenType.symbol and ctoken != ":":
                    raise OSParserError("Expected false condition operator here: %s" % (ctoken))
                self._advance()
                ctype, ctoken = self.__current

                rhs = self._expression()

                return OSConditionalExpressionNode(cond, true=lhs, false=rhs)

        return OSExpressionNode(oper, lhs, rhs)

    def _type(self):
        """Get a type, if available.

        Returns: Either an `OSOptionalTypeNode` for an optional type
        or an `OSTypeNode` containing the type in question.

        Raises: `OSParserError` if the type passed was not a primitive
        type or a type that was previously defined before.
        """
        ctype, ctoken = self.__current
        is_list = False

        if ctype == OSTokenType.symbol and ctoken == "[":
            is_list = True
            self._advance()
            ctype, ctoken = self.__current

        if ctype != OSTokenType.identifier and ctype != OSTokenType.keyword:
            raise OSParserError("Expected an identifier or keyword here: %s" % ctoken)
        if ctoken not in self._standard_types and ctoken not in self.__newtypes:
            raise OSParserError("%s is not a valid type." % ctoken)

        typename = ctoken

        self._advance()
        ctype, ctoken = self.__current

        if ctype == OSTokenType.symbol and ctoken == "?":
            return OSOptionalTypeNode(possible_value=None, possible_type=ctype)
        elif ctype == OSTokenType.symbol and ctoken == "]" and is_list:
            return OSListTypeReferenceNode(content_type=typename)
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
        """Get a type declaration, if available.

        Returns: `OSTypeDeclarationNode` if a type was declared.

        Raises: `OSParserError` if the parsing of the type declaration failed.
        """
        ctype, ctoken = self.__current

        if ctype != OSTokenType.keyword and ctoken != "type":
            raise OSParserError("Expected type declaration keyword.")

        self._advance()
        ctype, ctoken = self.__current

        if ctype != OSTokenType.identifier:
            raise OSParserError("Expected type identifier but received %s instead."
                                % (ctoken))

        new_type_name = ctoken
        new_type_extends = None

        self._advance()
        ctype, ctoken = self.__current

        if ctype != OSTokenType.symbol and ctoken != "=":
            raise OSParserError("Expected type declaration assignment here.")

        self._advance()
        ctype, ctoken = self.__current

        if ctype != OSTokenType.keyword and ctoken not in self._standard_types:
            raise OSParserError("Expected a standard type but received %s instead." % (ctoken))

        new_type_extends = ctoken
        self.__newtypes.append(new_type_name)

        return OSTypeDeclarationNode(new_type_name, new_type_extends)

    def _datatype_options(self):
        """Get a data type option declaration list, if available.

        Returns: A list of `OSDatatypeOptionNode` with all of the data type options.

        Raises: `OSParserError` if the parsing of data type options fails.
        """
        options = []
        ctype, ctoken = self.__current

        if ctype != OSTokenType.identifier:
            raise OSParserError("Expected identifier for datatype option.")

        f_id = ctoken
        f_types = []

        self._advance()
        ctype, ctoken = self.__current

        while ctype == OSTokenType.keyword and\
            (ctoken in self._standard_types or ctoken in self.__newtypes):
            f_types.append(self._type())
            self._advance()
            ctype, ctoken = self.__current

        self.__newtypes.append(f_id)
        options.append(OSDatatypeOptionNode(f_id, f_types))

        self._advance()
        ctype, ctoken = self.__current

        if ctype == OSTokenType.keyword and ctoken == "or":
            while ctype == OSTokenType.keyword and ctoken == "or":
                self._advance()
                ctype, ctoken = self.__current

                if ctype != OSTokenType.identifier:
                    raise OSParserError("Expected identifier for datatype option.")

                o_id = ctoken
                o_types = []

                self._advance()
                ctype, ctoken = self.__current

                while ctype == OSTokenType.keyword and\
                    (ctoken in self._standard_types or ctoken in self.__newtypes):
                    o_types.append(self._type())
                    self._advance()
                    ctype, ctoken = self.__current

                self.__newtypes.append(o_id)
                options.append(OSDatatypeOptionNode(o_id, o_types))

        return options


    def _datatype_declaration(self):
        """Get a datatype declaration, if available.

        Returns: `OSDatatypeDeclarationNode` containing the data type information.

        Raises: `OSParserError` if parsing the datatype declaration fails.
        """
        ctype, ctoken = self.__current

        if ctype != OSTokenType.keyword and ctoken != "datatype":
            raise OSParserError("Expected datatype declaration keyword here.")

        self._advance()
        ctype, ctoken = self.__current

        if ctype != OSTokenType.identifier:
            raise OSParserError("Expected datatype identifier here.")

        data_type_name = ctoken
        data_type_options = []

        self._advance()
        ctype, ctoken = self.__current

        if ctype != OSTokenType.symbol and ctoken != '=':
            raise OSParserError("Expected datatype declaration assignment here.")

        self._advance()
        ctype, ctoken = self.__current

        if ctype != OSTokenType.identifier:
            raise OSParserError("Expected identifier for datatype option.")

        data_type_options = self._datatype_options()
        self.__newtypes.append(data_type_name)

        return OSDatatypeDeclarationNode(data_type_name, None, data_type_options)

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
                elif ctoken == "module":
                    break
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

        if not name.startswith("ocellus_"):
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
                raise OSParserError("Cannot instantiate parser with both a script\
                                    and list of tokens.")
            self._tokens = tokens

        self._tree = []
        self.__current = self.__previous = None, None
        self.__newtypes = self.__newfuncs = []

if __name__ == "__main__":
    SOURCE = """
module Test where

example t = (t > 5) ? t : 8
    """
    MYPARSE = OSParser(SOURCE)
    p = MYPARSE.parse()
    print(p)
