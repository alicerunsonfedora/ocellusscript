"""
The `ast` submodule of Efficacy contains the classes used inside of the
Efficacy parser.
"""

#
# OcellusScript Tree Classes
# (C) 2020 Marquis Kurt.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

class _OSNode(object):
    """An OcellusScript base node.

    Attributes:
        root: The root value, or the top of this tree.
        lhs: The left branch of this tree, or None if this is a leaf.
        rhs: The right branch of this tree, or None if this is a leaf.
    """
    def __init__(self, root, lhs=None, rhs=None):
        """Construct a basic node.

        Arguments:
            root: The root value, or the top of this tree.
            lhs: The left branch of this tree, or None if this is a leaf.
            rhs: The right branch of this tree, or None if this is a leaf.
        """
        self.root = root
        self.lhs = lhs
        self.rhs = rhs

class OSTypeNode(_OSNode):
    """An OcellusScript type definition node.

    This node is often used to either create a type definition for type signatures
    or to act as the parent class for node with types containing values (i.e., in
    expression evaluation).

    Attributes:
        typename: The name of the type to define.
        typevalue: The value of the type.
    """
    def __init__(self, typename, typevalue):
        """Construct a type node.

        Attributes:
            typename: The name of the type to define.
            typevalue: The value of the type.
        """
        _OSNode.__init__(self, root=typevalue)
        self.type = typename

class OSNothingTypeNode(OSTypeNode):
    """An OcellusScript type node to represent the `Nothing` type.

    This node is a leaf node and does not take any additional parameters.
    """
    def __init__(self):
        """Construct a Nothing node."""
        OSTypeNode.__init__(self, typename="Nothing", typevalue=None)

class OSAnythingTypeNode(OSTypeNode):
    """An OcellusScript type node to represent the `Anything` type.

    This node is typically a leaf node or a parent class for primitive
    data types such as Character, String, or Integer.
    """
    def __init__(self, value, special_type=None):
        """Construct an Anything node.

        Arguments:
            value: The value of this type.
            special_type: The type that this value uses, if deriving from Anything.
        """
        OSTypeNode.__init__(self, typename=special_type if special_type else "Anything",
                            typevalue=value)

class OSErrorTypeNode(OSTypeNode):
    """An OcellusScript type node to represent the `Error` type.

    This node is a leaf node and does not take any additional parameters. The error
    content is stored as this type's value.
    """
    def __init__(self, error):
        """Construct an Error node.

        Arguments:
            error: The value or message of this Error node.
        """
        OSTypeNode.__init__(self, typename="Error", typevalue=error)

class OSCharacterTypeNode(OSAnythingTypeNode):
    """An OcellusScript character type node.

    The Character type node subclasses from the Anything type node and uses
    its value as the value of this node.
    """
    def __init__(self, value):
        """Construct a character type node.

        Arguments:
            value: The character value to store.
        """
        OSAnythingTypeNode.__init__(self, value, special_type="Character")

class OSStringTypeNode(OSAnythingTypeNode):
    """An OcellusScript string type node.

    The String type node subclasses from the Anything type node and uses its
    value as the value of this node.
    """
    def __init__(self, value):
        """Construct a string type node.

        Arguments:
            value: The string value to store.
        """
        OSAnythingTypeNode.__init__(self, value, special_type="String")

class OSIntTypeNode(OSAnythingTypeNode):
    """An OcellusScript integer type node.

    The Integer type node subclasses from the Anything type node and uses its
    value as the value of this node.
    """
    def __init__(self, value):
        OSAnythingTypeNode.__init__(self, value, special_type="Integer")

class OSFloatTypeNode(OSAnythingTypeNode):
    """An OcellusScript float type node.

    The Float type node subclasses from the Anything type node and uses its
    value as the value of this node.
    """
    def __init__(self, value):
        OSAnythingTypeNode.__init__(self, value, special_type="Float")

class OSBooleanTypeNode(OSAnythingTypeNode):
    """An OcellusScript boolean type node.

    The Boolean type node subclasses from the Anything type node and uses its
    value as the value of this node.
    """
    def __init__(self, value):
        OSAnythingTypeNode.__init__(self, value, special_type="Boolean")

class OSListTypeNode(OSAnythingTypeNode):
    """An OcellusScript list type node.

    The List type node is a subclass of the Anything type node and sets the type
    name to "List" and the tree containing all of the list values as the value of
    this type. Additionally, the `list_type` attribute is set to define the items'
    type for this list.

    Attributes:
        list_type: the list's primitive type (String, Character, etc.)
    """
    def __init__(self, values, content_type):
        """Construct a List type node.

        Arguments:
            values: The tree containing the values of this list.
            content_type: The type of list.
        """
        OSAnythingTypeNode.__init__(self, value=values, special_type="List")
        self.list_type = content_type

class OSOptionalTypeNode(OSTypeNode):
    """An OcellusScript Optional type node.

    The Optional type node subclasses from OSTypeNode and contains the possible type
    and possible value. The root of the tree and the left branch contain the possible
    value, while the right branch contains a Nothing type node.
    """
    def __init__(self, possible_value, possible_type="Anything"):
        """Construct an optional type node.

        Arguments:
            possible_value: The potential value of this node.
            possible_type: The potential type of this node. Defaults to "Anything".
        """
        OSTypeNode.__init__(self, typename="Optional", typevalue=possible_type)
        self.lhs = possible_value
        self.rhs = OSNothingTypeNode()

class OSListTypeReferenceNode(OSTypeNode):
    """An OcellusScript list type reference node.

    This node is only used to identify when a List is being used as a type
    in a type signature. For list nodes, use `OSListTypeNode`.
    """
    def __init__(self, content_type):
        """Construct a list type reference node.

        Arguments:
            content_type: The list's item type.
        """
        OSTypeNode.__init__(self, typename="List", typevalue=content_type)

class OSExpressionNode(_OSNode):
    """An OcellusScript expression node.

    An expression node contains the operation in question as the root of
    the node and the values to perform the operation with as its branches.
    Operations that have specific associativity should make sure that the
    correct branch assignments are being used.
    """
    def __init__(self, operation, left, right):
        """Construct an expression node.

        Arguments:
            operation: The operation that will be performed on the tree's
            children.
            left: The first value of the operation.
            right: The second value of the operation.
        """
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

class OSFunctionReturnNode(_OSNode):
    """A basic representation of a function return node."""
    def __init__(self, name, params, defines_inline=False, inline_func=None):
        _OSNode.__init__(self, name)
        self.params = params
        self.defines_inline = defines_inline
        self.inline_func = inline_func

class OSModuleNode(OSFunctionNode):
    """A basic representation of a module node."""
    def __init__(self, name, assocated_fns, dependencies=None):
        OSFunctionNode.__init__(self, name, result=assocated_fns)
        self.dependencies = dependencies
