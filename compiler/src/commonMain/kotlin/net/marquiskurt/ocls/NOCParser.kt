/*
 * OcellusScript Parser
 * (C) 2020 Marquis Kurt.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import kotlin.random.Random

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

    private lateinit var tree: NOCModule

    /**
     * Advance to the next token in the queue.
     *
     * @param skipComments Whether to skip over comment tokens. Defaults to true.
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
     */
    @ExperimentalStdlibApi
    fun parse(): NOCModule {
        if (tokens == null) {
            this.tokenizer = NOCTokenizer(this.fromScript ?: "")
            this.tokens = this.tokenizer.tokenizeAll()
        }

        this.advanceToken()
        this.tree = this.parseModule()

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
                this.advanceToken();
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
            this.advanceToken();

            if (this.token != Pair(TokenType.SYMBOL, ";")) { throw Exception("Expected end of module statement.") }
            this.advanceToken()
        }

        while (listOf(TokenType.KEYWORD, TokenType.IDENTIFIER).contains(this.token.first)) {
            when (this.token.first) {
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

    private fun parseRootExpression(): NOCExpression {
        return NOCExpression("", null, null)
    }

}