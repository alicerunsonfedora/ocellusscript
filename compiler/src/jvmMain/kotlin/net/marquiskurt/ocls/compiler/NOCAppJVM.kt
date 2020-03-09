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

import NOCTokenizer
import NOCParser
import TokenType
import NOCAppArgs
import NOCAppParseTreeWriter
import NOCAppTokenWriter
import NOCModule


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
    private lateinit var tokenizer: NOCTokenizer

    /**
     * The parser to perform parsing operations on.
     *
     * This field is usually instantiated by methods such as `parseFile`.
     */
    private lateinit var parser: NOCParser

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
        this.tokenizer = NOCTokenizer(this.script)
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
        this.tokenizer = NOCTokenizer(this.script)
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

    /**
     * Parse the contents of a single file.
     *
     * @param index The index of the file in the file list to parse.
     * @return The parsed module tree from the file.
     */
    @ExperimentalStdlibApi
    fun parseFile(index: Int): NOCModule {
        if (this.files == null) {
            throw FileNotFoundException("Cannot tokenize an empty directory.")
        } else {
            this.script = this.files?.get(index)?.readText() ?: ""
        }
        this.parser = NOCParser(null, fromScript = this.script)
        return this.parser.parse()
    }

    /**
     * Parse the contents of a file.
     *
     * @param file The file object to read and parse from.
     * @return The parsed module tree from the file.
     */
    @ExperimentalStdlibApi
    fun parseFile(file: File): NOCModule {
        if (file == null) { throw FileNotFoundException("Cannot tokenize an empty file.") }
        this.script = file.readText()
        this.parser = NOCParser(null, fromScript = this.script)
        return this.parser.parse()
    }

    /**
     * Parse the contents of a directory.
     *
     * @return A list of parsed tree modules.
     */
    @ExperimentalStdlibApi
    fun parseDir(): List<NOCModule> {
        if (this.files == null) { throw FileNotFoundException("Cannot parse an empty directory.") }
        return this.files!!.map { file -> this.parseFile(file) }
    }

}

@ExperimentalStdlibApi
fun main(args: Array<String>) {
    ArgParser(args).parseInto(::NOCAppArgs).run {
        // Create the file object from the source folder.
        val sObj = File(source)

        if (verbose && sObj.isDirectory) {
            println("INFO: ${sObj.absolutePath} is a directory.\nApplying operations to all files in this directory...")
        }

        // Create a list of files, either from the directory or a single file.
        // In the case of the directory, only read the files that are OcellusScript
        // files (i.e., files with the 'ocls' extension).
        val files = if (sObj.isFile) { arrayOf(sObj) }
        else { sObj.listFiles{ _, name ->  name.contains(".ocls")} }

        // Initialize the app.
        val app = NOCAppJVM(files)

        // Store our trees.
        val trees = app.parseDir()

        // Write our token files if the token file parameter is passed.
        if (exportTokens) {
            // Store our token lists.
            val tokens = app.tokenizeDir()

            // Write multiple files that match the directory if we're looking at a dir.
            if (File(destination).isDirectory) {
                val tokenFiles = files.map { file -> file.name.replace(".ocls", ".noct") }
                for (pair in tokenFiles.zip(tokens)) {
                    val fileWriter = NOCAppTokenWriter(pair.second)
                    if (verbose) {
                        println("Writing token file ${pair.first} " +
                                "from ${pair.first.replace(".noct", ".ocls")}...")
                    }
                    fileWriter.writeFile("$destination/${pair.first}", pair.first)
                }
            }

            // Otherwise, treat it regularly.
            else {
                for (token in tokens) {
                    val fileWriter = NOCAppTokenWriter(token)
                    if (verbose) {
                        println("Writing token file to $destination...")
                    }
                    fileWriter.writeFile("$destination", destination)
                }
            }
        }

        // If we need to export our trees, write the XML versions of those trees.
        if (exportTree) {

            // Write over every tree in the directory.
            if (File(destination).isDirectory) {
                val treeFiles = files.map { file -> file.name.replace(".ocls", ".xml") }
                for (pair in treeFiles.zip(trees)) {
                    val fileWriter = NOCAppParseTreeWriter(pair.second, pair.first)
                    if (verbose) {
                        println("Writing pared XML file ${pair.first} " +
                                "from ${pair.first.replace(".xml", ".ocls")}...")
                    }
                    fileWriter.writeFile()
                }
            }

            // Otherwise, treat it as a single file.
            else {
                for (tree in trees) {
                    val fileWriter = NOCAppParseTreeWriter(tree, destination)
                    if (verbose) {
                        println("Writing parsed XML file to $destination...")
                    }
                    fileWriter.writeFile()
                }
            }
        }

    }
}
