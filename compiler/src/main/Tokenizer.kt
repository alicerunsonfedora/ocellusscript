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
    var integer: Int = 0
    var float: Double = 0.0
    var currentChar: Char = '\n'

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
        this.currentChar = this.chars.first()
        this.chars = this.chars.drop(1)
        return this.currentChar
    }

    /**
     * Unread the current character.
     */
    fun unread() {
        this.chars = listOf(this.currentChar).asIterable() + this.chars
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
        this.integer = 0
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

    /**
     * Determine whether the identifier is a keyword.
     *
     * @param identifier The identifier to look up
     * @return Boolean indicating that the identifier is a keyword
     */
    fun isKeyword(identifier: String): Boolean {
        val keywords = listOf("func", "class", "lambda", "takes", "returns",
                              "String", "Char", "Integer", "Float", "List",
                              "Anything", "Nothing", "Callable", "Boolean",
                              "shadowtype", "type", "import", "private",
                              "module", "and", "or", "not", "match", "var",
                              "let", "true", "false", "self", "super", "return")
        return keywords.contains(identifier)
    }

    /**
     * Get the TokenKeyword of an identifier, or throw an error if the identifier
     * is not a keyword.
     *
     * @param identifier The identifier to convert to a keyword enum
     * @return The keyword enum value
     */
    fun getKeyword(identifier: String): TokenKeyword {
        var key: TokenKeyword = TokenKeyword.SELF

        if (!this.isKeyword(identifier)) {
            throw NoSuchElementException("Supplied identifier is not a keyword.")
        }

        when (identifier) {
            "func" -> { key = TokenKeyword.FUNC }
            "class" -> { key = TokenKeyword.CLASS }
            "lambda" -> { key = TokenKeyword.LAMBDA }
            "takes" -> { key = TokenKeyword.TAKES }
            "returns" -> { key = TokenKeyword.RETURNS }
            "return" -> { key = TokenKeyword.RETURN }
            "String" -> { key = TokenKeyword.STRING }
            "Char" -> { key = TokenKeyword.CHAR }
            "Integer" -> { key = TokenKeyword.INTEGER }
            "Float" -> { key = TokenKeyword.FLOAT }
            "List" -> { key = TokenKeyword.LIST }
            "Anything" -> { key = TokenKeyword.ANYTHING }
            "Nothing" -> { key = TokenKeyword.NOTHING }
            "Callable" -> { key = TokenKeyword.CALLABLE }
            "Boolean" -> { key = TokenKeyword.BOOLEAN }
            "shadowtype" -> { key = TokenKeyword.SHADOWTYPE }
            "type" -> { key = TokenKeyword.TYPE }
            "import" -> { key = TokenKeyword.IMPORT }
            "module" -> { key = TokenKeyword.MODULE }
            "private" -> { key = TokenKeyword.PRIVATE }
            "and" -> { key = TokenKeyword.AND }
            "or" -> { key = TokenKeyword.OR }
            "not" -> { key = TokenKeyword.NOT }
            "match" -> { key = TokenKeyword.MATCH }
            "var" -> { key = TokenKeyword.VAR }
            "let" -> { key = TokenKeyword.LET }
            "true" -> { key = TokenKeyword.TRUE }
            "false" -> { key = TokenKeyword.FALSE }
            "self" -> { key = TokenKeyword.SELF }
            "super" -> { key = TokenKeyword.SUPER }
        }

        return key
    }

    /**
     * Advance and generate a single token.
     */
    fun advance() {
        var state = TokenizerState.START
        var tokenType: TokenType? = null
        var token: String = ""
        var curr: Char = '\n'
        var docstate: Int = 0

        while (state != TokenizerState.FINISH && state != TokenizerState.ERROR) {

            if (!this.hasMoreChars()) { return }
            curr = this.getNextChar()

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
                            when (curr) {
                                '#' -> {
                                    tokenType = TokenType.COMMENT
                                    state = TokenizerState.IN_ID
                                }
                                '`' -> {
                                    tokenType = TokenType.SYMBOL
                                    state = TokenizerState.MAYBE_DOCSTRING_START
                                    docstate += 1
                                }
                                else -> {
                                    tokenType = TokenType.SYMBOL
                                    state = TokenizerState.IN_ID
                                }
                            }
                        }
                    }

                    if (tokenType != null && tokenType != TokenType.STR_CONST) {
                        token += curr
                    }
                }
                TokenizerState.IN_ID -> {
                    when (tokenType) {
                        TokenType.IDENTIFIER -> {
                            if (!curr.isLetter() && curr != '_') {
                                state = TokenizerState.FINISH
                                this.unread()
                            } else { token += curr }
                        }
                        TokenType.STR_CONST -> {
                            if (curr == '"') {
                                state = TokenizerState.FINISH;
                                this.unread()
                            }
                            else { token += curr }
                        }
                        TokenType.INT_CONST -> {
                            if (!curr.isDigit() && curr != '.') {
                                state = TokenizerState.FINISH
                                this.unread()
                            } else {
                                if (curr == '.') { tokenType = TokenType.FLO_CONST }
                                token += curr
                            }
                        }
                        TokenType.FLO_CONST -> {
                            if (!curr.isDigit()) {
                                state = TokenizerState.FINISH
                                this.unread()
                            } else { token += curr }
                        }
                        TokenType.COMMENT -> {
                            if (curr == '\n') {
                                state = TokenizerState.FINISH
                                this.unread()
                            }
                        }
                        TokenType.SYMBOL -> {
                            state = TokenizerState.FINISH
                            this.unread()
                        }
                        TokenType.DOCSTRING -> {
                            if (curr == '`') {
                                state = TokenizerState.MAYBE_DOCSTRING_END
                                docstate += 1
                            }
                            token += curr
                        }
                        else -> {}
                    }
                }
                TokenizerState.MAYBE_DOCSTRING_START -> {
                    if (curr != '`') {
                        state = TokenizerState.IN_ID
                        this.unread()
                    } else {
                        if (docstate == 3) {
                            state = TokenizerState.IN_ID
                            tokenType = TokenType.DOCSTRING
                            docstate = 0
                        }
                        else { docstate += 1 }
                        token += curr
                    }
                }
                TokenizerState.MAYBE_DOCSTRING_END -> {
                    if (curr != '`') {
                        state = TokenizerState.IN_ID
                    } else {
                        if (docstate == 3) {
                            state = TokenizerState.FINISH
                            docstate = 0
                        }
                        else { docstate += 1 }
                    }
                    token += curr
                }
                else -> {
                    state = TokenizerState.ERROR
                }
            }
        }

        if (state != TokenizerState.ERROR) {
            if (this.isKeyword(token)) {
                tokenType = TokenType.KEYWORD
            }

            when (tokenType) {
                TokenType.KEYWORD -> {
                    this.keyword = this.getKeyword(token)
                    this.identifier = token
                }
                TokenType.IDENTIFIER -> { this.identifier = token }
                TokenType.COMMENT -> { this.comment = token }
                TokenType.DOCSTRING -> { this.docstring = token }
                TokenType.STR_CONST -> { this.identifier = token }
                TokenType.SYMBOL -> { this.symbol = token.first() }
                TokenType.INT_CONST -> { this.integer = token.toInt() }
                TokenType.FLO_CONST -> { this.float = token.toDouble() }
            }

            this.tokenType = tokenType
        }
    }

    /**
     * Tokenize the entire character list, rather than just advancing over a single token.
     */
    fun tokenizeAll(): List<Pair<TokenType?, String>?> {
        var tokens: List<Pair<TokenType?, String>?> = listOf(null)

        while (hasMoreChars() && this.tokenType != null) {
            this.resetToken()
            this.advance()
            when (this.tokenType) {
                TokenType.STR_CONST -> { tokens += listOf(Pair(this.tokenType, this.identifier)) }
                TokenType.INT_CONST -> { tokens += listOf(Pair(this.tokenType, this.integer.toString()))}
                TokenType.FLO_CONST -> { tokens += listOf(Pair(this.tokenType, this.float.toString()))}
                TokenType.COMMENT -> { tokens += listOf(Pair(this.tokenType, this.comment)) }
                TokenType.DOCSTRING -> { tokens += listOf(Pair(this.tokenType, this.docstring)) }
                TokenType.SYMBOL -> { tokens += listOf(Pair(this.tokenType, this.symbol.toString()))}
                TokenType.IDENTIFIER -> { tokens += listOf(Pair(this.tokenType, this.identifier))}
                TokenType.KEYWORD -> { tokens += listOf(Pair(this.tokenType, this.identifier))}
                else -> {}
            }
        }

        return tokens
    }

}