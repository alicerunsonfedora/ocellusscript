/*
 * NOCExtensionSuite.kt
 * (C) 2020 Marquis Kurt.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

package net.marquiskurt.ocls

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
 * Get the longest String in a list of strings.
 *
 * @return The longest string in the list.
 */
fun List<String>.longest(): String {
    var big = this.first()
    for (string in this.subList(1, this.size - 1)) {
        if (string.length > big.length) { big = string }
    }
    return big
}