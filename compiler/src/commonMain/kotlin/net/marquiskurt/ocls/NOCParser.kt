/*
 * OcellusScript Parser
 * (C) 2020 Marquis Kurt.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import kotlin.random.Random

import net.marquiskurt.ocls.longest

/**
 * The NOC OcellusScript parser.
 *
 * The parser is responsible for reading a list of tokens and creating an abstract syntax tree.
 */
class NOCParser(private var tokens: List<Pair<TokenType?, String>?>? = null,
                private var fromScript: String? = null) {

    /**
     * A tokenizer to generate tokens from, if necessary.
     */
    private lateinit var tokenizer: NOCTokenizer

    /**
     * The current token in the parsing queue.
     */
    private lateinit var token: Pair<TokenType?, String>

    /**
     * The entire abstract syntax tree for a given list of tokens or script.
     */
    private lateinit var tree: NOCModule

    /**
     * Advance to the next token in the queue.
     *
     * @param skipComments Whether to skip over comment tokens. Defaults to `true`.
     * @return The current token at the front of the queue.
     */
    private fun advanceToken(skipComments: Boolean = true): Pair<TokenType?, String> {
        if (this.tokens?.count() ?: -1 > 0) {
            this.token = this.tokens!!.first()!!
            this.tokens = this.tokens!!.drop(1)

            while (this.token.first == TokenType.COMMENT && skipComments) {
                this.token = this.tokens!!.first()!!
                this.tokens = this.tokens!!.drop(1)
            }
        }
        return this.token
    }

    /**
     * Look ahead to the next token in the queue without advancing.
     *
     * @return The next token in the queue, or `null` if none exist.
     */
    private fun lookahead(): Pair<TokenType?, String>? {
        return this.tokens?.first()
    }

    /**
     * Generate an abstract syntax tree.
     *
     * @return The parsed abstract syntax tree as an `NOCModule`
     */
    @ExperimentalStdlibApi
    fun parse(): NOCModule {

        // Generate the list of tokens if we have a script but no tokens to work with.
        if (tokens == null) {
            this.tokenizer = NOCTokenizer(this.fromScript ?: "")
            this.tokens = this.tokenizer.tokenizeAll()
        }

        // Pre-load the first token.
        this.advanceToken()

        // Parse the module.
        this.tree = this.parseModule()

        // Return the tree.
        return this.tree
    }

    /**
     * Generate a completely random module name.
     *
     * This is typically used when the module in question does not have a name (i.e., cannot be imported
     * into other code).
     *
     * @return String containing "_ModuleOcls_", followed by 9 random digits.
     */
    private fun createModuleName(): String {
        val randInts = List(9) { Random.nextInt(0, 9).toString() }
        return "_ModuleOcls_" + randInts.reduceRight { curr, acc -> curr + acc }
    }

    /**
     * Create an OcellusScript module, the root tree.
     *
     * @return NOCModule containing all of the code from the module.
     */
    @ExperimentalStdlibApi
    private fun parseModule(): NOCModule {

        // Create an empty module state. Since we don't know if this module has a name, we'll assign
        // a temporary one first.
        var name = this.createModuleName()
        var imports: MutableList<String>? = null
        var datatypes: MutableList<NOCType>? = null
        var shadowtypes: MutableList<NOCShadowType>? = null
        var variables: MutableList<NOCVariableDeclaration>? = null
        var classes: MutableList<NOCClass>? = null
        var funcs: MutableList<NOCFunction>? = null

        // Look for any import statements and construct those imports.
        while (this.token == Pair(TokenType.KEYWORD, "import")) {
            this.advanceToken()
            var importName = ""
            if (this.token.first != TokenType.IDENTIFIER) {
                throw Exception("Expected import name identifier here: ${this.token.second}")
            }

            importName += this.token.second
            this.advanceToken()

            if (this.token.first == TokenType.SYMBOL) {
                if (!".!*".contains(this.token.second.toCharArray()[0])) {
                    throw Exception("Unexpected symbol in import statement: ${this.token.second}")
                }
                importName += this.token.second
                this.advanceToken()
                if (this.token.first != TokenType.SYMBOL && this.token.first != TokenType.IDENTIFIER) {
                    throw Exception("Unexpected ${this.token.first.toString()} " +
                            "found in import name: ${this.token.second}")
                }

                if (this.token.first == TokenType.SYMBOL && this.token.second != "*") {
                    throw Exception("Unexpected symbol in import name: ${this.token.second}")
                }

                importName += this.token.second
                this.advanceToken()

                if (this.token != Pair(TokenType.SYMBOL, ";")) { throw Exception("Expected end of import statement.") }
                this.advanceToken()

                if (imports == null) { imports = mutableListOf(importName) }
                else { imports.add(importName) }
            }
        }

        // If there's an actual name for this module, change our state.
        if (this.token == Pair(TokenType.KEYWORD, "module")) {
            this.advanceToken()

            if (this.token.first != TokenType.IDENTIFIER) { throw Exception("Expected module name identifier here: " +
                    this.token.second)}
            name = this.token.second
            this.advanceToken()

            if (this.token != Pair(TokenType.KEYWORD, "where")) { throw Exception("Expected where keyword here: " +
                    this.token.second)}
            this.advanceToken()

            if (this.token != Pair(TokenType.SYMBOL, ";")) { throw Exception("Expected end of module statement.") }
            this.advanceToken()
        }

        // Check for all identifiers and keywords and create separate statements and declarations for
        // each.
        while (listOf(TokenType.KEYWORD, TokenType.IDENTIFIER).contains(this.token.first)) {
            when (this.token.first) {

                // If we're looking at a keyword, filter through all possible keywords and create
                // the respective statements.
                TokenType.KEYWORD -> {
                    when (this.token.second) {
                        "shadowtype" -> {
                            if (shadowtypes != null) { shadowtypes.add(this.parseShadowtype()) }
                            else { shadowtypes = mutableListOf(this.parseShadowtype()) }
                        }
                        "type" -> {
                            if (datatypes != null) { datatypes.add(this.parseDatatype()) }
                            else { datatypes = mutableListOf(this.parseDatatype()) }
                        }
                        "var" -> {
                            if (variables != null) { variables.add(this.parseVarDeclaration().declare) }
                            else {variables = mutableListOf(this.parseVarDeclaration().declare)}
                        }
                        "let" -> {
                            if (variables != null) { variables.add(this.parseLetDeclaration().declare) }
                            else {variables = mutableListOf(this.parseLetDeclaration().declare)}
                        }
                        else -> {}
                    }
                }
                else -> {}
            }
            this.advanceToken()
        }

        // Finally, put the state together and return the module.
        return NOCModule(name, imports, datatypes, shadowtypes, variables, classes, funcs)
    }

    /**
     * Create an OcellusScript shadow type node.
     *
     * @return NOCShadowType data object containing the name and type.
     */
    @ExperimentalStdlibApi
    private fun parseShadowtype(): NOCShadowType {

        if (this.token != Pair(TokenType.KEYWORD, "shadowtype")) {
            throw Exception("Expected shadowtype keyword here: ${this.token.second}")
        }
        this.advanceToken()

        if (this.token.first != TokenType.IDENTIFIER) {
            throw Exception("Expected shadowtype name identifier here: ${this.token.second}")
        }
        val name: String = this.token.second
        this.advanceToken()

        if (this.token != Pair(TokenType.SYMBOL, "=")) {
            throw Exception("Expected shadowtype assignment operator here: ${this.token.second}")
        }
        this.advanceToken()

        if (this.token.first != TokenType.IDENTIFIER && this.token.first != TokenType.KEYWORD) {
            throw Exception("Expected shadowtype assignment here: ${this.token.second}")
        }
        val shadow: String = this.token.second
        this.advanceToken()

        if (this.token != Pair(TokenType.SYMBOL, ";")) {
            throw Exception("Expected end of shadowtype statement: ${this.token.second}")
        }
        return NOCShadowType(name, shadow)
    }

    /**
     * Create an OcellusScript datatype node.
     *
     * @return NOCType object containing the name and all possible options
     */
    @ExperimentalStdlibApi
    private fun parseDatatype(): NOCType {
        var options: MutableList<String>

        if (this.token != Pair(TokenType.KEYWORD, "type")) {
            throw Exception("Expected type keyword here: ${this.token.second}")
        }
        this.advanceToken()

        if (this.token.first != TokenType.IDENTIFIER) {
            throw Exception("Expected type name identifier here: ${this.token.second}")
        }
        val name: String = this.token.second
        this.advanceToken()

        if (this.token != Pair(TokenType.SYMBOL, "=")) {
            throw Exception("Expected type assignment operator here: ${this.token.second}")
        }
        this.advanceToken()

        if (this.token != Pair(TokenType.SYMBOL, "{")) {
            throw Exception("Expected type assignment here: ${this.token.second}")
        }
        this.advanceToken()

        var option = this.parseDatatypePair()
        options = mutableListOf(option)
        this.advanceToken()

        while (this.token == Pair(TokenType.SYMBOL, ",")) {
            this.advanceToken()
            option = this.parseDatatypePair()
            options = mutableListOf(option)
            this.advanceToken()
        }

        if (this.token != Pair(TokenType.SYMBOL, "}")) {
            throw Exception("Expected end of type assignment here: ${this.token.second}")
        }
        this.advanceToken()

        if (this.token != Pair(TokenType.SYMBOL, ";")) {
            throw Exception("Expected end of type statement: ${this.token.second}")
        }

        return NOCType(name, options)
    }

    /**
     * Create a datatype option string.
     *
     * @return A string containing the key-value pair in a datatype option
     */
    @ExperimentalStdlibApi
    private fun parseDatatypePair(): String {
        if (this.token.first != TokenType.IDENTIFIER) {
            throw Exception("Expected type option key here: ${this.token.second}")
        }

        var option = this.token.second + ": "
        this.advanceToken()
        if (this.token != Pair(TokenType.SYMBOL, ":")) {
            throw Exception("Expected key separator here: ${this.token.second}")
        }
        this.advanceToken()

        if (this.token != Pair(TokenType.SYMBOL, "(")) {
            throw Exception("Expected value opening parentheses here: ${this.token.second}")
        }
        this.advanceToken()

        while (this.token != Pair(TokenType.SYMBOL, ")")) {
            option += this.token.second + " "
            this.advanceToken()
        }

        if (this.token != Pair(TokenType.SYMBOL, ")")) {
            throw Exception("Expected value closing parentheses here: ${this.token.second}")
        }
        return option
    }

    /**
     * Create an OcellusScript variable declaration statement using `var`.
     *
     * @return NOCVarStatement object containing the the declared variable.
     */
    @ExperimentalStdlibApi
    private fun parseVarDeclaration(): NOCVarStatement {
        if (this.token != Pair(TokenType.KEYWORD, "var")) {
            throw Exception("Expected var keyword in variable declaration: ${this.token.second}")
        }
        this.advanceToken()
        if (this.token.first != TokenType.IDENTIFIER) {
            throw Exception("Expected var name identifier here: ${this.token.second}")
        }
        val name = this.token.second
        this.advanceToken()
        if (this.token != Pair(TokenType.SYMBOL, "=")) {
            throw Exception("Expected var declaration assignment operator: ${this.token.second}")
        }
        this.advanceToken()
        val store = this.parseRootExpression()
        this.advanceToken()

        if (this.token != Pair(TokenType.SYMBOL, ";")) {
            throw Exception("Expected end of var statement: ${this.token.second}")
        }

        return NOCVarStatement(NOCVariableDeclaration(name, "Anything", store))
    }

    /**
     * Create an OcellusScript constant declaration using the `let` statement.
     *
     * @return NOCLetStatement object containing the declared constant value
     */
    @ExperimentalStdlibApi
    private fun parseLetDeclaration(): NOCLetStatement {
        if (this.token != Pair(TokenType.KEYWORD, "let")) {
            throw Exception("Expected var keyword in constant declaration: ${this.token.second}")
        }
        this.advanceToken()
        if (this.token.first != TokenType.IDENTIFIER) {
            throw Exception("Expected const name identifier here: ${this.token.second}")
        }
        val name = this.token.second
        this.advanceToken()
        if (this.token != Pair(TokenType.SYMBOL, "=")) {
            throw Exception("Expected var declaration assignment operator: ${this.token.second}")
        }
        this.advanceToken()
        val store = this.parseRootExpression()
        this.advanceToken()

        if (this.token != Pair(TokenType.SYMBOL, ";")) {
            throw Exception("Expected end of let statement: ${this.token.second}")
        }

        return NOCLetStatement(NOCVariableDeclaration(name, "Anything", store, const = true))
    }

    private fun parseFunctionCall(): NOCFunctionReturn {
        return NOCFunctionReturn("", listOf())
    }

    /**
     * Parse an expression based on a set of rules.
     *
     * If operators in the list have more than one character, the operator will be checked by reading more tokens.
     * This is usually done by checking the longest value in the string list (`List<String>.longest`).
     *
     * @param validOperators The list containing the valid operations in this expression tree.
     * @param notBasic Whether the expression is not a 'basic' expression
     * @param elements The function to return the children NOCExpression objects.
     * @return NOCExpression containing the operation and root children. The operation is set to `value` if no other
     * operator is found.
     */
    @ExperimentalStdlibApi
    private fun parseExpression(validOperators: List<String>, notBasic: Boolean = false,
                                elements: () -> NOCExpression): NOCExpression {

        // Set the default values. Left is excluded because the left child will always be created
        // first.
        var right: NOCExpression? = null
        var operation = "value"

        // Convert the valid operators to a list of characters with unique characters.
        val chars = validOperators
                .map { op -> op.toCharArray().toMutableList() }
                .reduce { x, y -> (x + y).toMutableList() }
                .distinct()

        // Create the left side of the tree and advance to the next token if we're not parsing
        // a basic expression.
        val left = elements()
        if (notBasic) { this.advanceToken() }

        // Create the operator and evaluate the right side of the expression afterwards.
        if (listOf(TokenType.SYMBOL, TokenType.KEYWORD).contains(this.token.first)
                && chars.contains(this.token.second[0])) {

            operation = this.token.second

            if (this.token.first == TokenType.SYMBOL) {
                if (validOperators.longest().length > 1) {
                    for (x in (2 .. validOperators.longest().length)) {
                        this.advanceToken()
                        if (this.token.first != TokenType.SYMBOL) {
                            throw Exception("Unexpected ${this.token.first} in operation: ${this.token.second}")
                        }
                        operation += this.token.second
                        if (validOperators.contains(operation)) { break }
                    }
                }
            }

            // If we have a valid operator, advance and evaluate the right side of the tree.
            if (validOperators.contains(operation)) {
                this.advanceToken()
                right = elements()
            }

        }

        // Finally, return the entire expression node.
        return NOCExpression(operation, left, right)
    }

    /**
     * Create a 'basic expression' node.
     *
     * @return NOCExpression either containing a parenthetical expression or a single
     * node with no children.
     */
    @ExperimentalStdlibApi
    private fun parseBasicExpression(): NOCExpression {
        var expr = NOCExpression("null", null, null)
        when (this.token.first) {
            null -> { throw Exception("Null token not acceptable here in this context.") }

            // Check for any tokens with a symbol and evaluate them as either nested expressions
            // or as list literals.
            TokenType.SYMBOL -> {
                when (this.token.second) {
                    "(" -> {
                        this.advanceToken()
                        expr = this.parseRootExpression()
                        this.advanceToken()
                    }
                    "[" -> {
                        // TODO: Write logic for list expression parsing here.
                    }
                    else -> {throw Exception("Unexpected symbol in basic expression: ${this.token.second}")}
                }
            }

            // If a keyword, verify whether the keyword is a valid keyword in the context and use that.
            TokenType.KEYWORD -> {
                val keywordConstants = listOf("true", "false", "self", "super", "Nothing")
                if (!keywordConstants.contains(this.token.second)) {
                    throw Exception("Unexpected keyword in expression ${this.token.second}")
                }
                expr = NOCExpression(this.token.second, null, null)
            }

            // TODO: Make special cases for identifiers.
            TokenType.IDENTIFIER -> {
                val next = this.lookahead()
                if (next != null) {
                    if (next.first == TokenType.SYMBOL) {
                        when (this.token.second) {
//                            "(" -> { expr = this.parseFunctionCall() }
                            "[" -> {}
                            "{" -> {}
                            else -> {}
                        }
                    } else {
                        expr = NOCExpression(this.token.second, null, null)
                    }
                }
            }
            // Otherwise, for any other type, create a leaf node.
            else -> expr = NOCExpression(this.token.second, null, null)
        }
        return expr
    }

    /**
     * Parse a multiplicative expression.
     *
     * This a convenience method of `NOCParser.parseExpression` that checks for multiplicative operators
     * before proceeding to create a basic expression.
     *
     * @return NOCExpression with a multiplicative operator.
     *
     * @see NOCParser.parseExpression
     */
    @ExperimentalStdlibApi
    private fun parseMultiplicativeExpression(): NOCExpression {
        return this.parseExpression(listOf("*", "/", "%"), true) { this.parseBasicExpression() }
    }

    /**
     * Parse a additive expression.
     *
     * This a convenience method of `NOCParser.parseExpression` that checks for additive operators
     * before proceeding to create a multipicative expression.
     *
     * @return NOCExpression with a additive operator.
     *
     * @see NOCParser.parseExpression
     */
    @ExperimentalStdlibApi
    private fun parseAdditiveExpression(): NOCExpression {
        return this.parseExpression(listOf("+", "-")) { this.parseMultiplicativeExpression() }
    }

    /**
     * Parse a "high inequal" expression.
     *
     * This a convenience method of `NOCParser.parseExpression` that checks for "high inequal" operators
     * before proceeding to create an additive expression.
     *
     * "High inequal" operators refer to raw comparison operators (>, <), excluding equality, since these
     * operators take higher precedence than lower inequal operators.
     *
     * @return NOCExpression with a "high inequal" operator.
     *
     * @see NOCParser.parseExpression
     */
    @ExperimentalStdlibApi
    private fun parseHighInequalExpression(): NOCExpression {
        return this.parseExpression(listOf(">", "<")) { this.parseAdditiveExpression() }
    }

    /**
     * Parse a "low inequal" expression.
     *
     * This a convenience method of `NOCParser.parseExpression` that checks for "low inequal" operators
     * before proceeding to create a "high inequal" expression.
     *
     * "Low inequal" operators refer to raw comparison operators, equality inclusive (>=, <=).
     *
     * @return NOCExpression with a "low inequal" operator.
     *
     * @see NOCParser.parseExpression
     */
    @ExperimentalStdlibApi
    private fun parseLowInqeualExpression(): NOCExpression {
        return this.parseExpression(listOf(">=", "<=")) { this.parseHighInequalExpression() }
    }

    /**
     * Parse an equality expression.
     *
     * This a convenience method of `NOCParser.parseExpression` that checks for equality operators
     * before proceeding to create a "low inequal" expression.
     *
     * @return NOCExpression with an equality operator.
     *
     * @see NOCParser.parseExpression
     */
    @ExperimentalStdlibApi
    private fun parseEqualityExpression(): NOCExpression {
        return this.parseExpression(listOf("!=", "==")) { this.parseLowInqeualExpression() }
    }

    /**
     * Parse a boolean expression.
     *
     * This a convenience method of `NOCParser.parseExpression` that checks for boolean operators
     * before proceeding to create an equality expression, excluding `not`.
     *
     * @return NOCExpression with a boolean operator.
     *
     * @see NOCParser.parseExpression
     */
    @ExperimentalStdlibApi
    private fun parseBooleanExpression(): NOCExpression {
        return this.parseExpression(listOf("and", "or")) { this.parseEqualityExpression() }
    }

    /**
     * Create an OcellusScript expression node.
     *
     * This function invokes `NOCParser.parseBooleanExpression` and runs down the chain to create
     * the entire expression tree.
     *
     * @return NOCExpression object containing the expression tree.
     */
    @ExperimentalStdlibApi
    private fun parseRootExpression(): NOCExpression {
        return this.parseBooleanExpression()
    }

}