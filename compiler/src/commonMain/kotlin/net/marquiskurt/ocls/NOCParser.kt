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
        var datatypes: List<NOCType>? = null
        var shadowtypes: List<NOCShadowType>? = null
        var variables: List<NOCVariableDeclaration>? = null
        var classes: List<NOCClass>? = null
        var funcs: List<NOCFunction>? = null

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

        // TODO: Add stuff for parsing variables, classes, functions, etc., here.

        // Finally, put the state together and return the module.
        return NOCModule(name, imports, datatypes, shadowtypes, variables, classes, funcs)
    }

}