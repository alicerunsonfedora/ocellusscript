/*
 * NOCAppParseTreeWriter.kt
 * (C) 2020 Marquis Kurt.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import java.io.File

class NOCAppParseTreeWriter(private val tree: NOCModule, var destinationPath: String) {

    private var fileWriter = File(this.destinationPath).writer()

    /**
     * Write a single child element.
     *
     * @param tagName The name of the tag to use.
     * @param child The string element to insert as the child of this tag.
     */
    private fun writeChild(tagName: String, child: String) {
        fileWriter.write("<$tagName> $child </$tagName>\n")
    }

    /**
     * Write a single child element.
     *
     * @param tagName The name of tag to use
     * @param children The function to run to write the children of this tag.
     */
    private fun writeChild(tagName: String, children: () -> Unit) {
        fileWriter.write("<${tagName}>\n")
        children()
        fileWriter.write("</${tagName}>\n")
    }

    /**
     * Write the tree into a parsable XML file.
     */
    fun writeFile() {
        this.writeChild("module") {
            this.writeChild("name", this.tree.name)
            if (this.tree.imports != null) {
                this.writeChild("dependencies") {
                    for (dependency: String in this.tree.imports) {
                        this.writeChild("dependency", dependency)
                    }
                }
            }
        }
        this.fileWriter.close()
    }
}