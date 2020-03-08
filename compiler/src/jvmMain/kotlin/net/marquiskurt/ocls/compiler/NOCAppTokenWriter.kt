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

class NOCAppTokenWriter(tokens: List<Pair<TokenType?, String>?>) {

    /**
     * Write the token file.
     *
     * @param destinationPath The destination path and filename.
     */
    fun writeFile(destinationPath: String) {
        var fileObj = File(destinationPath)
    }

}
