/*
 * NOC Tokenizer File Author
 * (C) 2020 Marquis Kurt.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import java.io.File

import TokenType

class NOCAppTokenWriter(val tokens: List<Pair<TokenType?, String>?>) {

    /**
     * Write the token file.
     *
     * @param destinationPath The destination path and filename.
     */
    fun writeFile(destinationPath: String) {
        var fileObj = if (File(destinationPath).isDirectory) { File("$destinationPath/tokens.noct") }
            else { File(destinationPath) }

        var writer = fileObj.writer()

        for (token in this.tokens) {
            if (token != null) {
                writer.write("${token.first} ${token.second}\n")
            }
        }
        writer.close()
    }
}
