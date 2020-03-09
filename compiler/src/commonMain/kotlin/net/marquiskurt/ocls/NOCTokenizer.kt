/**
 * OcellusScript Tokenizer
 * (C) 2020 Marquis Kurt.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/**
 * Determine whether a character is a letter.
 */
fun Char.isLetter(): Boolean {
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".contains(this)
}

/**
 * Determine whether a character is a numerical digit.
 */
fun Char.isDigit(): Boolean {
    return "0123456789".contains(this)
}

/**
 * The NOC OcellusScript tokenizer.
 *
 * The tokenizer is responsible for reading a string and generating a list of
 * tokens that can later be used for parsing.
 */
class NOCTokenizer(private var script: String) {

    @ExperimentalStdlibApi
    private var chars: CharArray = this.script.toCharArray()

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
    @ExperimentalStdlibApi
    fun hasMoreChars(): Boolean {
        return this.chars.count() > 0
    }

    /**
     * Grab the next character if it exists.
     */
    @ExperimentalStdlibApi
    fun getNextChar(): Char {
        if (!hasMoreChars()) {
            throw NoSuchElementException("There are no more characters to process.")
        }
        this.currentChar = this.chars.first()
        this.chars = this.chars.drop(1).toCharArray()
        return this.currentChar
    }

    /**
     * Unread the current character.
     */
    @ExperimentalStdlibApi
    fun unread() {
        this.chars = listOf(this.currentChar).toCharArray() + this.chars
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
        val symbols: String = "+-/%*?:,.;<>=`_()[]{}#"
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
    @ExperimentalStdlibApi
    fun advance() {

        // Create an empty state with default values.
        var state = TokenizerState.START
        var tokenType: TokenType? = null
        var token = ""
        var curr: Char
        var docstate = 0

        // Loop while the state is unfinished.
        while (state != TokenizerState.FINISH && state != TokenizerState.ERROR) {

            // Exit out of this loop if there are no more characters.
            if (!this.hasMoreChars()) { break }

            // Pop the current character off the queue.
            curr = this.getNextChar()

            when (state) {

                // Determine the type of token at the beginning stages.
                TokenizerState.START -> {
                    when {

                        // If the character is a letter, choose identifier.
                        curr.isLetter() -> {
                            tokenType = TokenType.IDENTIFIER
                            state = TokenizerState.IN_ID
                        }

                        // If a digit, mark as an integer.
                        curr.isDigit() -> {
                            tokenType = TokenType.INT_CONST
                            state = TokenizerState.IN_ID
                        }

                        // More special cases for symbols.
                        this.isSymbol(curr) -> {
                            when (curr) {

                                // Mark as a comment.
                                '#' -> {
                                    tokenType = TokenType.COMMENT
                                    state = TokenizerState.IN_ID
                                }

                                // Mark as a possible docstring.
                                '`' -> {
                                    tokenType = TokenType.SYMBOL
                                    state = TokenizerState.MAYBE_DOCSTRING_START
                                    docstate += 1
                                }

                                // Mark as a string.
                                '"' -> {
                                    tokenType = TokenType.STR_CONST
                                    state = TokenizerState.IN_ID
                                }

                                // Otherwise, treat as a regular symbol.
                                else -> {
                                    tokenType = TokenType.SYMBOL
                                    state = TokenizerState.IN_ID
                                }
                            }
                        }
                    }

                    // After defining the token type, if the type isn't a string, add the character to our token.
                    if (tokenType != null && tokenType != TokenType.STR_CONST) {
                        token += curr
                    }
                }

                // Determine when to stop processing the token (or when to add the current character to the token).
                TokenizerState.IN_ID -> {
                    when (tokenType) {

                        // If an identifier and the character isn't a letter or an underscore, exit.
                        TokenType.IDENTIFIER -> {
                            if (!curr.isLetter() && curr != '_') {
                                state = TokenizerState.FINISH
                                this.unread()
                            } else { token += curr }
                        }

                        // If a string and we find the end quote, exit.
                        TokenType.STR_CONST -> {
                            if (curr == '"') {
                                state = TokenizerState.FINISH;
                                this.unread()
                            }
                            else { token += curr }
                        }

                        // If an integer and the character isn't a period or a number, exit.
                        // If the character IS a period, change the type to a float and keep
                        // processing.
                        TokenType.INT_CONST -> {
                            if (!curr.isDigit() && curr != '.') {
                                state = TokenizerState.FINISH
                                this.unread()
                            } else {
                                if (curr == '.') { tokenType = TokenType.FLO_CONST }
                                token += curr
                            }
                        }

                        // If a float and the character isn't a number, exit.
                        TokenType.FLO_CONST -> {
                            if (!curr.isDigit()) {
                                state = TokenizerState.FINISH
                                this.unread()
                            } else { token += curr }
                        }

                        // If a comment and the character is a newline character, exit.
                        TokenType.COMMENT -> {
                            if (curr == '\n') {
                                state = TokenizerState.FINISH
                                this.unread()
                            } else { token += curr }
                        }

                        // If a symbol, exit.
                        TokenType.SYMBOL -> {
                            state = TokenizerState.FINISH
                            this.unread()
                        }

                        // If a docstring and the character is the docstring backtick, change the state.
                        TokenType.DOCSTRING -> {
                            if (curr == '`') {
                                state = TokenizerState.MAYBE_DOCSTRING_END
                                docstate += 1
                            }
                            token += curr
                        }

                        // Ignore any other types.
                        else -> {}
                    }
                }

                // Keep checking for new characters that match the backtick. When we've determined there are three
                // backticks in a row, assume that we're looking at a docstring and change the state.
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

                // Keep checking for new characters that match the backtick. When we've determined there are three
                // backticks in a row, assume that we've found the end of the docstring and exit the state.
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

                // Other states will result in error.
                else -> { state = TokenizerState.ERROR }
            }
        }

        // If the state has NOT errored in the process, finalize the token and set the proper attributes of this class.
        if (state != TokenizerState.ERROR) {

            // Look for a keyword.
            if (this.isKeyword(token)) { tokenType = TokenType.KEYWORD }

            // Set the different fields of this class based on the current token type.
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

            // Set the type of the token to the class's attribute.
            this.tokenType = tokenType
        }
    }

    /**
     * Tokenize the entire character list, rather than just advancing over a single token.
     */
    @ExperimentalStdlibApi
    fun tokenizeAll(): List<Pair<TokenType?, String>?> {
        val tokens: MutableList<Pair<TokenType?, String>?> = mutableListOf(null)

        while (this.hasMoreChars() || this.tokenType != null) {
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
        if (tokens.first() == null) { tokens.remove(null) }
        return tokens
    }

}