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

class OSOptionalTypeNode(OSTypeNode):
    """A basic representation of an optional type node."""
    def __init__(self, possible_value, possible_type="Anything"):
        OSTypeNode.__init__(self, typename="Optional", typevalue=possible_type)
        self.lhs = possible_value
        self.rhs = OSNothingTypeNode()

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
    def __init__(self, name, input, output):
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
    def __init__(self, name, assocated_fns):
        OSFunctionNode.__init__(self, name, result=assocated_fns)

class OSParser(object):
    """The parsing class for OcellusScript.

    The parser is responsible for reading a list of tokens and converting
    the them into a traversable abstract syntax treee that can be used to
    compile into a program with LLVM or can be processed differently with
    a Python script.
    """

    _current = None
    _tokenizer = OSTokenizer("")
    _tokens = []
    _tree = []

    def _advance(self):
        """Get the next token in the list, if available."""
        if len(self._tokens) > 0:
            self._current = self._tokens.pop(0)

    def _keyword_constant(self, keyword):
        """Get an appropriate keyword constant node, if available."""
        if keyword not in ["true", "false", "Anything", "Nothing"]:
            raise OSParserError("%s is not a valid keyword constant." % (keyword))

        if keyword == "true" or keyword == "false":
            return OSBooleanTypeNode(value=keyword)
        elif keyword == "Anything":
            return OSAnythingTypeNode(value=None)
        else:
            return OSNothingTypeNode()

    def _basic_expression(self):
        current_type, current_token = self._current
        if current_type == OSTokenType.string:
            return OSStringTypeNode(value=current_token)
        elif current_type == OSTokenType.num_integer:
            return OSIntTypeNode(value=current_token)
        elif current_type == OSTokenType.num_float:
            return OSFloatTypeNode(value=current_token)
        elif current_type == OSTokenType.keyword:
            return self._keyword_constant(current_token)
        elif current_type == OSTokenType.symbol and current_token == "(":
            return self._expanded_expression()
        else:
            raise OSParserError("%s is not a valid expression in this context." % (current_token))

    def _multiplicative_expression(self):
        current_type, current_token = self._current
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
        raise NotImplementedError()

    def _signature(self):
        current_type, current_token = self._current
        if current_type != OSTokenType.identifier:
            raise OSParserError("Type signature expects an identifier here.")
        name = current_token
        self._advance()
        
        if current_type != OSTokenType.keyword or current_token != "takes":
            raise OSParserError("'takes' is expected here in type signature.")

        inputs = []
        self._advance()
        raise NotImplementedError()

    def _function(self):
        current_type, current_token = self._current
        if current_type == OSTokenType.identifier:
            possible_signature_name = current_token
            self._signature()

        if current_type == OSTokenType.identifier:
            self._signature()

    def parse(self):
        """Parse through the list of tokens or script and return the expression
        tree, if there are no errors.

        If an error occurs during the parsing processing, the parser throws an
        `OSParserError`.

        Returns: A list containing the abstract syntax tree of the OcellusScript
        code.
        """
        if not self._tokens and self._tokenizer.source:
            self._tokens = self._tokenizer.tokenize()
        return self._tree

    def __init__(self, script="", tokens=None):
        """Construct the parser object.

        When constructing this object, either a script that can be tokenized
        can be passed or a list of existing tokens. Do not pass both a script
        and a list of tokens; doing this will result in an `OSParserError` being
        thrown.

        Args:
            script: The script to tokenize and then parse.
            tokens: A pre-existing list tokens to parse.
        """
        self._tokenizer = OSTokenizer(script)

        if tokens:
            if script:
                raise OSParserError("Cannot instantiate parser with a script and list of tokens.")
            self._tokens = tokens
