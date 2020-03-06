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
     * Generate the next token, when ready.
     */
    fun advance() {
        var state = TokenizerState.START
        var tokenType: TokenType? = null
        var token = ""
        var curr = this.getNextChar()
    }

}