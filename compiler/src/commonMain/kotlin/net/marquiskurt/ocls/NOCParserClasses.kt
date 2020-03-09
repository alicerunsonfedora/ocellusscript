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
                     val classes: List<NOCClass>?)

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
data class NOCVariableDeclaration(val name: String, val type: String, val value: String?)

/**
 * A data representation of an OcellusScript function signature.
 */
data class NOCFunctionSignature(val name: String, val inputs: List<String>, val returns: List<String>)

/**
 * A data representation of an OcellusScript expression tree node.
 */
data class NOCExpression(val operation: String, val left: NOCExpression?, val right: NOCExpression?)

/**
 * A data representation of an OcellusScript function return call.
 */
data class NOCFunctionReturn(val funcCallName: String, val params: List<NOCExpression>?)

/**
 * A data representation of an OcellusScript class.
 */
data class NOCClass(val name: String, val fields: List<NOCVariableDeclaration>?)