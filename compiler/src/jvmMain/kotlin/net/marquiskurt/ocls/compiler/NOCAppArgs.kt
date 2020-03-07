/**
 * NOC for JVM Arguments
 * (C) 2020 Marquis Kurt.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import com.xenomachina.argparser.ArgParser

/**
 * The base class containing all of the arguments for NOC.
 */
class NOCArgs(parser: ArgParser) {
    val verbose by parser.flagging(
        "-v", "--verbose",
        help="Run NOC in verbose mode.")
    val exportTokens by parser.flagging(
        "--output-tokens",
        help="Whether to output a file containing the tokens.")
    val exportTree by parser.flagging(
        "--output-abstract-tree",
        help="Whether to output a file containing the parsed tree.")
    val source by parser.positional(
        "SOURCE",
        help="The directory or input file to compile.")
    val destination by parser.positional(
        "DEST",
        help="The destination filename for the compiled file.")
}