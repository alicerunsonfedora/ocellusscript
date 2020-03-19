/*
 * NOCParserClasses.kt
 * (C) 2020 Marquis Kurt.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/**
 * A data representation of an OcellusScript module.
 */
data class NOCModule(val name: String,
                     val imports: List<String>?,
                     val datatypes: List<NOCType>?,
                     val types: List<NOCShadowType>?,
                     val vars: List<NOCVariableDeclaration>?,
                     val classes: List<NOCClass>?,
                     val functions: List<NOCFunction>?)

/**
 * A data representation of an OcellusScript shadow type.
 */
data class NOCShadowType(val name: String, val shadows: String)

/**
 * A data representation of an OcellusScript type.
 */
data class NOCType(val name: String, val options: List<String>)

/**
 * A data representation of an OcellusScript var declaration.
 */
data class NOCVariableDeclaration(val name: String,
                                  val type: String,
                                  val value: NOCExpression,
                                  val const: Boolean = false)

/**
 * A data representation of an OcellusScript function signature.
 */
data class NOCFunctionSignature(val name: String, val inputs: List<String>, val returns: List<String>)

/**
 * A data representation of an OcellusScript list pair.
 *
 * Lists typically use this structure.
 */
data class NOCListPair(val head: NOCExpression, val tail: NOCListPair?)

/**
 * A data representation of an OcellusScript expression tree node.
 */
data class NOCExpression(val operation: String,
                         val fnReturn: NOCFunctionReturn? = null,
                         val list: NOCListPair? = null,
                         val left: NOCExpression? = null,
                         val right: NOCExpression? = null)

/**
 * A data representation of an OcellusScript function return call.
 */
data class NOCFunctionReturn(val funcCallName: String, val params: List<NOCExpression>?)

/**
 * A data representation of an OcellusScript `let` statement.
 */
data class NOCLetStatement(val declare: NOCVariableDeclaration)

/**
 * A data representation of an OcellusScript `var` statement.
 *
 * For storage of a variable, use `NOCVariableDeclaration` instead.
 */
data class NOCVarStatement(val declare: NOCVariableDeclaration)

/**
 * A data representation of an OcellusScript `while` statement.
 */
data class NOCWhileStatement(val iterateOver: NOCExpression, val statements: List<Any>?)

/**
 * A data class representation of an OcellusScript `for` statement.
 */
data class NOCForStatement(val iter: String, val range: NOCExpression, val statements: List<Any>?)

/**
 * A data representation of an OcellusScript `return` statement.
 */
data class NOCReturnStatement(val result: NOCExpression?)

/**
 * A data representation of a match case.
 */
data class NOCMatchCase(val case: NOCExpression, val expression: NOCExpression?, val statements: List<Any>?)

/**
 * A data representation of an OcellusScript `match` statement.
 */
data class NOCMatch(val over: NOCExpression, val cases: List<NOCMatchCase>)

/**
 * A data representation of an OcellusScript function.
 */
data class NOCFunction(val name: String,
                       val signature: NOCFunctionSignature?,
                       val docstring: String?,
                       val statements: List<Any>?,
                       val result: NOCExpression?)

/**
 * A data representation of an OcellusScript class.
 */
data class NOCClass(val name: String, val fields: List<NOCVariableDeclaration>?, val methods: List<NOCFunction>?)