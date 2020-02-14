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
        type: The name of the type to define.
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

class OSTypeDeclarationNode(OSTypeNode):
    """An OcellusScript custom type declaration node.

    Custom type declarations subclass from `OSTypeNode` and often shadow an existing
    type.

    Attributes:
        extends_type: The primitive type that the custom type draws from.
    """
    def __init__(self, name, extends, value=None):
        """Construct a custom type declaration node.

        Arguments:
            name: The name of the custom type.
            extends: The primitive type that this custom type shadows.
            value: The value of the type, if any. Defaults to None.
        """
        OSTypeNode.__init__(self, typename=name, typevalue=value)
        self.extends_type = extends

    def raw_type(self):
        """Return the primitive or 'raw' version of this type."""
        if self.extends_type == "Character":
            return OSCharacterTypeNode(value=self.root)
        elif self.extends_type == "String":
            return OSStringTypeNode(value=self.root)
        elif self.extends_type == "Integer":
            return OSIntTypeNode(value=self.root)
        elif self.extends_type == "Float":
            return OSFloatTypeNode(value=self.root)
        elif self.extends_type == "Boolean":
            return OSBooleanTypeNode(value=self.root)
        elif self.extends_type == "Anything":
            return OSAnythingTypeNode(value=self.root)
        else:
            return OSNothingTypeNode()

class OSDatatypeDeclarationNode(OSTypeNode):
    """An OcellusScript data type declaration node.

    Custom data type nodes sublass from `OSTypeNode` and define their own structures
    of how data is organized.

    Attributes:
        options: The different options that define this data type.
    """
    def __init__(self, name, value, options):
        """Construct a datatype declaration node.

        Arguments:
            name: The name of the custom data type
            value: The assigned value of this data type, if any.
            options: The options for this data type.
        """
        OSTypeNode.__init__(self, name, value)
        self.options = options

class OSDatatypeOptionNode(OSTypeNode):
    """An OcellusScript data type option node.

    The data type option node is a subclass of `OSTypeNode` that defines an option for a data
    type. The `typename` is set to the option's identifier and `typevalue` is set to the list
    of primitive data types that follow it.
    """
    def __init__(self, name, types):
        OSTypeNode.__init__(self, typename=name, typevalue=types)

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
    """An OcellusScript conditional expression node.

    A conditional expression node contains the condition to evaluate for truthiness as the
    root of the node, with the left branch corresponding to the value or expression to use
    when the condition returns true, and the right branch corresponding to the value or
    expression to use when the condition returns false.
    """
    def __init__(self, condition, true=None, false=None):
        """Construct a contidional expression node.

        Arguments:
            condition: The condition to evaluate for truthiness.
            true: The expression or value to return when the condition is true.
            false: The expression or value to return when the condition is false.
        """
        OSExpressionNode.__init__(self, operation=condition, left=true, right=false)

class OSSignatureNode(_OSNode):
    """An OcellusScript type signature node.

    Type signature nodes contain the input type and output type information for a designated
    function and are usually an attribute of an `OSFunctionNode`. The root of the node contains
    the function's name, and the left and right branches contains the input types and output types,
    respectively.
    """
    def __init__(self, name, input, output): # pylint:disable=redefined-builtin
        """Construct a type signature node.

        Arguments:
            name: The name of the function associated with this signature
            input: The list of input types as parameters of this function
            output: The list of output types as the result of this function
        """
        _OSNode.__init__(self, root=name, lhs=input, rhs=output)

class OSFunctionNode(_OSNode):
    """An OcellusScript function node.

    A function node contains the information necessary to recreate a function. The root of this
    node is typically the result expression and does not use any child branches.

    Attributes:
        name: The name of the function
        types: The type signature of this function, if it exists.
        help: The docstring for this function, if it exists.
        private: Whether the function is considered a private function of a module.
        Defaults to False.
    """
    def __init__(self, name, result, signature=None, docstring=None, private=False):
        """Construct a function node.

        Arguments:
            name: The name of the function.
            result: The result expression of this function.
            signature: The type signature for this function, if any. Defaults to None.
            docstring: The help docstring for this function, if any. Defaults to None.
            private: Whether this function is private. Defaults to False.
        """
        _OSNode.__init__(self, root=result)
        self.name = name
        self.types = signature
        self.help = docstring
        self.private = private

class OSFunctionReturnNode(_OSNode):
    """An OcellusScript function return node.

    Function return nodes are used to indicate that an expression will use the result of a function
    with a given name and set of parameters. Function return nodes also can have inline functions
    that are defined, typically using the `where` statement.

    Attributes:
        params: The parameters passed to the function.
        defines_inline: Whether the function return includes a new function definition. Defaults to
        False.
        inline_func: The function definition if defines_inline is true. Defaults to None.
    """
    def __init__(self, name, params, defines_inline=False, inline_func=None):
        """Construct a function return node.

        Arguments:
            name: The name of the function being called.
            params: The list of parameters being called.
            defines_inline: Whether the call is defining a new function. Defaults to False.
            inline_func: The in-line function being defined. Defaults to None.
        """
        _OSNode.__init__(self, name)
        self.params = params
        self.defines_inline = defines_inline
        self.inline_func = inline_func

class OSModuleNode(OSFunctionNode):
    """An OcellusScript module node.

    Module nodes are subclassed from `OSFunctionNode` and are typically the root node of an
    OcellusScript file. Module nodes contain information such as dependencies from import
    statements and the root node consists of all of the functions defined in that module.

    Attributes:
        dependencies: The required modules to be imported.
    """
    def __init__(self, name, assocated_fns, dependencies=None):
        """Construct an OcellusScript module node.

        Arguments:
            name: The name of the module.
            associated_fns: The associated functions defined in this module.
            dependencies: The list of dependencies needed for this module. Defaults to none.
        """
        OSFunctionNode.__init__(self, name, result=assocated_fns)
        self.dependencies = dependencies
