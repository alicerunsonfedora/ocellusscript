/**
 * OcellusScript Tokenizer
 * (C) 2020 Marquis Kurt.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TokenType
import TokenizerState

public class OSTokenizer(var script: String) {

    private var chars: Iterable<Char> = this.script.asIterable()
    var tokenType: TokenType? = null
    var identifier: String = ""
    var symbol: Char = '\n'
    var comment: String = ""
    var docstring: String = ""
    var keyword: TokenKeyword? = null

    /**
     * Determine whether there are more characters to process.
     *
     * @return Boolean of whether chars is not empty
     */
    fun hasMoreChars(): Boolean {
        return this.chars.count() > 0
    }

    /**
     * Grab the next character if it exists.
     */
    fun getNextChar(): Char {
        if (!hasMoreChars()) {
            throw NoSuchElementException("There are no more characters to process.")
        }
        return this.chars.first()
    }

    /**
     * Reset the current token state.
     */
    fun resetToken() {
        this.tokenType = null
        this.identifier = ""
        this.symbol = '\n'
        this.comment = ""
        this.docstring = ""
    }

    /**
     * Determine whether a character is a symbol
     *
     * @param char The character to look up in the symbols
     * @return Boolean indicating if the character is a valid symbol
     */
    fun isSymbol(char: Char): Boolean {
        val symbols: String = "+-/%*?:,.;<>=`_()[]{}"
        return symbols.contains(char)
    }

    // fun isKeyword(identifier: String): Boolean {
    //     val keywords = TokenKeyword.values().apply { $it.toString() }
    //     return keywords.contains(identifier)
    // }

    /**
     * Generate the next token, when ready.
     */
    fun advance() {
        var state = TokenizerState.START
        var tokenType: TokenType? = null
        var token = ""
        var curr = this.getNextChar()

        while (state != TokenizerState.FINISH && state != TokenizerState.ERROR) {
            when (state) {
                TokenizerState.START -> {
                    when {
                        curr.isLetter() -> {
                            tokenType = TokenType.IDENTIFIER
                            state = TokenizerState.IN_ID
                        }
                        curr.isDigit() -> {
                            tokenType = TokenType.INT_CONST
                            state = TokenizerState.IN_ID
                        }
                        this.isSymbol(curr) -> {

                        }
                    }
                }
                TokenizerState.IN_ID -> {
                }
                else -> {

                }
            }
        }
    }

}