/*
 * NOC Tokenizer File Author
 * (C) 2020 Marquis Kurt.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import java.io.File

/**
 * The NOC token file writer.
 */
class NOCAppTokenWriter(val tokens: List<Pair<TokenType?, String>?>) {

    /**
     * Create an NOC token file.
     *
     * @param destinationPath The destination path and filename.
     * @param header The header to write at the top of the file.
     */
    fun writeFile(destinationPath: String, header: String = "TOKENS.OCLS") {
        val fileObj = if (File(destinationPath).isDirectory) { File("$destinationPath/tokens.noct") }
            else { File(destinationPath) }
        val writer = fileObj.writer()
        writer.write("${header.toUpperCase()}\n@BEGIN TOKEN CONSTRUCT\n")
        for (token in this.tokens) {
            if (token != null) {
                writer.write("${token.first} ${token.second}\n")
            }
        }
        writer.write("@END TOKEN CONSTRUCT")
        writer.close()
    }
}
