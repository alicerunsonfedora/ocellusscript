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
import java.io.FileNotFoundException

import OSTokenizer
import TokenType
import NOCArgs

/**
 * The primary app class for the NOC.
 */
class NOCAppJVM(private var files: Array<File>?) {

    /**
     * The String version of the file to tokenize and/or parse.
     *
     * This field is usually updated by methods such as `tokenizeFile`.
     */
    private var script = ""

    /**
     * The tokenizer to perform lexer operations on.
     *
     * This field is usually instantiated by methods such as `tokenizeFile`.
     */
    private lateinit var tokenizer: OSTokenizer

    /**
     * Tokenize the contents of a single file in the directory.
     *
     * @param index The element file to tokenize
     * @return A list containing all of the tokens from that file
     */
    @ExperimentalStdlibApi
    fun tokenizeFile(index: Int): List<Pair<TokenType?, String>?> {
        if (this.files == null) {
            throw FileNotFoundException("Cannot tokenize an empty directory.")
        } else {
            this.script = this.files?.get(index)?.readText() ?: ""
        }
        this.tokenizer = OSTokenizer(this.script)
        return this.tokenizer.tokenizeAll()
    }

    /**
     * Tokenize the contents of a single file in a directory.
     *
     * @param file the File object to tokenize
     * @return A list containing all of the tokens from that file
     */
    @ExperimentalStdlibApi
    fun tokenizeFile(file: File?): List<Pair<TokenType?, String>?> {
        if (file == null) { throw FileNotFoundException("Cannot tokenize an empty file.") }
        this.script = file.readText()
        this.tokenizer = OSTokenizer(this.script)
        return this.tokenizer.tokenizeAll()
    }

    /**
     * Tokenize all files in a directory.
     *
     * @return A list containing the list of tokens from each file.
     */
    @ExperimentalStdlibApi
    fun tokenizeDir(): List<List<Pair<TokenType?, String>?>> {
        if (this.files == null) {
            throw FileNotFoundException("Cannot tokenize an empty directory.")
        }

        return this.files!!.map { file -> this.tokenizeFile(file) }
    }

}

@ExperimentalStdlibApi
fun main(args: Array<String>) {
    ArgParser(args).parseInto(::NOCAppArgs).run {
        // Create the file object from the source folder.
        val sObj = File(source)

        // Create a list of files, either from the directory or a single file.
        // In the case of the directory, only read the files that are OcellusScript
        // files (i.e., files with the 'ocls' extension).
        val files = if (sObj.isFile) { arrayOf(sObj) }
        else { sObj.listFiles{ _, name ->  name.contains(".ocls")} }

        // Initialize the app.
        val app = NOCAppJVM(files)

        // Print out the list of token lists.
        println(app.tokenizeDir())
    }
}
