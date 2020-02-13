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

from efficacy.lexer import OSTokenizer, OSTokenType

class OSParserError(Exception):
    """The error to use when the parser has failed."""

class _OSNode(object):
    """A basic representation of a tree node."""
    def __init__(self, root, lhs=None, rhs=None):
        self.root = root
        self.lhs = lhs
        self.rhs = rhs

class OSTypeNode(_OSNode):
    """A basic representation of a type node."""
    def __init__(self, typename, typevalue):
        _OSNode.__init__(self, root=typevalue)
        self.type = typename

class OSNothingTypeNode(OSTypeNode):
    """A basic representation of a "Nothing" type."""
    def __init__(self):
        OSTypeNode.__init__(self, typename="Nothing", typevalue=None)

class OSAnythingTypeNode(OSTypeNode):
    """A basic representation of an Anything type."""
    def __init__(self, value, special_type=None):
        OSTypeNode.__init__(self, typename=special_type if special_type else "Anything",
                            typevalue=value)

class OSErrorTypeNode(OSTypeNode):
    """A basic representation of an Error type."""
    def __init__(self, error):
        OSTypeNode.__init__(self, typename="Error", typevalue=error)

class OSCharacterTypeNode(OSAnythingTypeNode):
    """A basic representation of a Character type."""
    def __init__(self, value):
        OSAnythingTypeNode.__init__(self, value, special_type="Character")

class OSStringTypeNode(OSAnythingTypeNode):
    """A basic representation of a String type."""
    def __init__(self, value):
        OSAnythingTypeNode.__init__(self, value, special_type="String")

class OSIntTypeNode(OSAnythingTypeNode):
    """A basic representation of an Integer type."""
    def __init__(self, value):
        OSAnythingTypeNode.__init__(self, value, special_type="Integer")

class OSFloatTypeNode(OSAnythingTypeNode):
    """A basic representation of a Float type."""
    def __init__(self, value):
        OSAnythingTypeNode.__init__(self, value, special_type="Float")

class OSBooleanTypeNode(OSAnythingTypeNode):
    """A basic representation of a Boolean type."""
    def __init__(self, value):
        OSAnythingTypeNode.__init__(self, value, special_type="Boolean")

class OSListTypeNode(OSAnythingTypeNode):
    """A basic representation of a list node."""
    def __init__(self, values, content_type):
        OSAnythingTypeNode.__init__(self, value=values, special_type="List")
        self.list_type = content_type

class OSOptionalTypeNode(OSTypeNode):
    """A basic representation of an optional type node."""
    def __init__(self, possible_value, possible_type="Anything"):
        OSTypeNode.__init__(self, typename="Optional", typevalue=possible_type)
        self.lhs = possible_value
        self.rhs = OSNothingTypeNode()

class OSListTypeReferenceNode(OSTypeNode):
    """A basic representation of a list type (reference).

    This node is typically used for type signatures.
    """
    def __init__(self, content_type):
        OSTypeNode.__init__(self, typename="List", typevalue=content_type)

class OSExpressionNode(_OSNode):
    """A basic representation of an expression node."""
    def __init__(self, operation, left=None, right=None):
        _OSNode.__init__(self, root=operation, lhs=left, rhs=right)

class OSConditionalExpressionNode(OSExpressionNode):
    """A basic representation of a conditional expression node."""
    def __init__(self, condition, true=None, false=None):
        OSExpressionNode.__init__(self, operation=condition, left=true, right=false)

class OSSignatureNode(_OSNode):
    """A basic representation of a type signature node."""
    def __init__(self, name, input, output): # pylint:disable=redefined-builtin
        _OSNode.__init__(self, root=name, lhs=input, rhs=output)

class OSFunctionNode(_OSNode):
    """A basic representation of a function node."""
    def __init__(self, name, result, signature=None, docstring=None, private=False):
        _OSNode.__init__(self, root=result)
        self.name = name
        self.types = signature
        self.help = docstring
        self.private = private

class OSModuleNode(OSFunctionNode):
    """A basic representation of a module node."""
    def __init__(self, name, assocated_fns, dependencies=None):
        OSFunctionNode.__init__(self, name, result=assocated_fns)
        self.dependencies = dependencies

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

        Returns: A subclassed `OSTypeNode`, or an `OSExpressionNode` if
        the expression contains operations.

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
            return self._expanded_expression()
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

    def _expanded_expression(self):
        raise NotImplementedError()

    def _type(self):
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

    def _fn_definition(self):
        ctype, ctoken = self.__current

        if ctype != OSTokenType.identifier:
            raise OSParserError("Expected a function identifier here: %s" % (ctoken))

        fn_name = ctoken

        if fn_name in self.__newfuncs:
            raise OSParserError("Function %s was already defined." % (fn_name))

        # TODO: Determine how to switch between signature and definition...



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
                raise OSParserError("Cannot instantiate parser with a script and list of tokens.")
            self._tokens = tokens

        self._tree = []
        self.__current = self.__previous = None, None
        self.__newtypes = self.__newfuncs = []
