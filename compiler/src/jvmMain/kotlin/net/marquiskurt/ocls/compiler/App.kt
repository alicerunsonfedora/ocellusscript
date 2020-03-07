/**
 * NOC for JVM
 * (C) 2020 Marquis Kurt.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package net.marquiskurt.ocls.compiler

import java.io.File
import com.xenomachina.argparser.ArgParser


import OSTokenizer
import TokenType


class NOC(val files: List<File>?) {

    private var script = ""
    private var tokenizer = OSTokenizer(this.script)

    @ExperimentalStdlibApi
    fun tokenize(): List<Pair<TokenType?, String?>?> {
        return this.tokenizer.tokenizeAll()
    }

}

// TODO: Process a directory or files with arguments
@ExperimentalStdlibApi
fun main(args: Array<String>) {
    println("TODO: Get this to make token files!")
}
