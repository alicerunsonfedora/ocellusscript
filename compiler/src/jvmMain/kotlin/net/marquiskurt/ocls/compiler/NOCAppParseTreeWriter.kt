/*
 * NOCAppParseTreeWriter.kt
 * (C) 2020 Marquis Kurt.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import java.io.File

/**
 * The NOC parser tree writer.
 *
 * The parser tree writer will generate a regular XML file with the parsed tokens of the
 * the given tree, stored in its destination path.
 */
class NOCAppParseTreeWriter(private val tree: NOCModule, var destinationPath: String) {

    private var fileWriter = File(this.destinationPath).writer(charset("UTF-8"))

    /**
     * Write a single child element.
     *
     * @param tagName The name of the tag to use.
     * @param child The string element to insert as the child of this tag.
     */
    private fun writeChild(tagName: String, child: String) {
        this.fileWriter.write("<$tagName> $child </$tagName>\n")
    }

    /**
     * Write a single child element.
     *
     * @param tagName The name of tag to use
     * @param children The function to run to write the children of this tag.
     */
    private fun writeChild(tagName: String, children: () -> Unit) {
        this.fileWriter.write("<${tagName}>\n")
        children()
        this.fileWriter.write("</${tagName}>\n")
    }

    /**
     * Write the tree into a parsable XML file.
     */
    fun writeFile() {
        this.fileWriter.write("<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n")
        this.writeChild("module") {
            this.writeChild("name", this.tree.name)
            if (this.tree.imports != null) {
                this.writeChild("dependencies") {
                    for (dependency: String in this.tree.imports) {
                        this.writeChild("dependency", dependency)
                    }
                }
            }

            if (this.tree.types != null) {
                this.writeChild("shadowtypes") {
                    for (shadowtype: NOCShadowType in this.tree.types) {
                        this.writeChild("shadowtype") {
                            this.writeChild("name", shadowtype.name)
                            this.writeChild("shadows", shadowtype.shadows)
                        }
                    }
                }
            }

            if (this.tree.datatypes != null) {
                this.writeChild("types") {
                    for (type: NOCType in this.tree.datatypes) {
                        this.writeChild("type") {
                            this.writeChild("name", type.name)
                            this.writeChild("options") {
                                for (option in type.options) {
                                    this.writeChild("option", option)
                                }
                            }
                        }
                    }
                }
            }
        }
        this.fileWriter.close()
    }
}