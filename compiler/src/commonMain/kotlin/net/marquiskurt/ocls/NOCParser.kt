/*
 * OcellusScript Parser
 * (C) 2020 Marquis Kurt.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import NOCModule
import NOCClass
import NOCShadowType
import NOCType
import NOCTokenizer

/**
 * The NOC OcellusScript parser.
 *
 * The parser is responsible for reading a list of tokens and creating an abstract syntax tree.
 */
class NOCParser(private var tokens: List<Pair<TokenType?, String>?>? = null, private var fromScript: String? = null) {

    /**
     * A tokenizer to generate tokens from, if necessary.
     */
    private lateinit var tokenizer: NOCTokenizer

    /**
     * The current token in the parsing queue.
     */
    private lateinit var token: Pair<TokenType?, String>

    /**
     * Advance to the next token in the queue.
     *
     * @param skipComments Whether to skip over comment tokens. Defaults to true.
     * @return The current token at the front of the queue.
     */
    private fun advanceToken(skipComments: Boolean = true): Pair<TokenType?, String> {
        this.token = this.tokens!!.first()!!
        this.tokens = this.tokens!!.drop(1)

        while (this.token.first == TokenType.COMMENT && skipComments) {
            this.token = this.tokens!!.first()!!
            this.tokens = this.tokens!!.drop(1)
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
    fun parse() {
        if (tokens == null) {
            this.tokenizer = NOCTokenizer(this.fromScript ?: "")
            this.tokens = this.tokenizer.tokenizeAll()
        }
    }

}