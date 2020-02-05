"""
The `cli` submodule of Efficacy contains the source code and functionality
for the command-line application version of the Efficacy compiler.
"""

#
# OcellusScript Efficacy CLI
# (C) 2020 Marquis Kurt.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

import argparse
import sys
import os
import json
from efficacy.lexer import OSTokenizer

def _generate_args():
    """Generate an argument parser based on the arguments needed for the
    compiler."""
    parser = argparse.ArgumentParser(usage='%(prog)s [options]')
    parser.description = "Efficacy is a compiler and interpreter environment for OcellusScript."
    parser.add_argument("-i", "--input",
                        nargs=1, metavar="file.ocls",
                        help="the input file to compile or run")
    parser.add_argument("-o", "--output",
                        nargs=1, metavar="exec",
                        help="the path to the compiled executable")
    parser.add_argument("-oT", "--output-tokens",
                        nargs=1, metavar="out.json",
                        help="the path to the JSON token file")
    return parser

def _make_token_file(input="", path=""):
    """Generate a tokenized JSON file that contains all of the tokens from
    a given source file."""
    source = ""
    lexer = OSTokenizer()
    json_contents = []

    with open(input, "r") as srcfile:
        source = srcfile.read()

    tokens = lexer.tokenize(source)

    for token_type, token in tokens:
        json_contents.append({token_type.value: token})

    with open(path, "w+") as out:
        out.writelines(json.dumps(json_contents, indent=4))

    return

def run_cli():
    """Start the main process for the CLI application."""
    parser = _generate_args()
    args = []

    if sys.argv[1:]:
        args = parser.parse_args(sys.argv[1:])

    if args:
        if args.input and args.output_tokens:
            for i, j in zip(args.input, args.output_tokens):
                _make_token_file(input=i, path=os.path.join(os.getcwd(), j))
    else:
        # TODO: Implement interactive mode
        print("Enter interactive mode here...")
