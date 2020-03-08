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
class NOCAppArgs(parser: ArgParser) {
    /**
     * Whether the program should run in verbose mode.
     */
    val verbose by parser.flagging(
        "-v", "--verbose",
        help="Run NOC in verbose mode.")

    /**
     * Whether the program should create OcellusScript token files.
     */
    val exportTokens by parser.flagging(
        "--output-tokens",
        help="Whether to output a file containing the tokens.")

    /**
     * Whether the program should create OcellusScript tree files.
     */
    val exportTree by parser.flagging(
        "--output-abstract-tree",
        help="Whether to output a file containing the parsed tree.")

    /**
     * The directory or file name to take in as input.
     */
    val source by parser.positional(
        "SOURCE",
        help="The directory or input file to compile.")

    /**
     * The destination file or directory to compile to.
     */
    val destination by parser.positional(
        "DEST",
        help="The destination filename for the compiled file.")
}