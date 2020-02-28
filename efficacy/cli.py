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
from efficacy.parser import OSParser, OSParserError

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
    parser.add_argument("-oA", "--output-abstract-tree",
                        nargs=1, metavar="out.json",
                        help="the path to the JSON abstract syntax tree file")
    parser.add_argument("-v", "--version",
                        nargs='?',
                        const=True,
                        help="display the version of Efficacy and exit")
    return parser

def _make_token_file(ifile="", ofile=""):
    """Generate a tokenized JSON file that contains all of the tokens from
    a given source file.

    Arguments:
        ifile: The path to the input file to tokenize.
        ofile: The path to the JSON file to write the tokens to.
    """
    source = ""
    json_contents = []

    # Exit if we aren't dealing with an OcellusScript file.
    if not ifile.endswith(".ocls"):
        print("%s is not an OcellusScript file. Aborting." % (ifile))
        return

    # Get the source from the input file.
    with open(ifile, "r") as srcfile:
        source = srcfile.read()

    # Tokenize the source.
    lexer = OSTokenizer(script=source)
    tokens = lexer.tokenize()

    # Generate the JSON object of all the tokens and types.
    if tokens:
        for token_type, token in tokens:
            token_key = token_type if isinstance(token_type, str) else token_type.value
            json_contents.append({token_key: token})

    # Write the file to JSON.
    with open(ofile, "w+") as out:
        out.writelines(json.dumps(json_contents, indent=4))

    return

def _make_parser_file(ifile="", ofile=""):
    """Generate an AST JSON file that contains the abstract syntax tree of the given
    input file.

    Arguments:
        ifile: The path to the input file to parse.
        ofile: The path to the JSON file to write the tree to.
    """
    source = ""
    tree = {}

    # Exit if we aren't dealing with an OcellusScript file.
    if not ifile.endswith(".ocls"):
        print("%s is not an OcellusScript file. Aborting." % (ifile))
        return

    with open(ifile, "r") as srcfile:
        source = srcfile.read()

    parser = OSParser(script=source)

    try:
        tree = parser.parse()
    except OSParserError as err:
        print("Failed to parse %s.\nException: %s" % (ifile, err))
        sys.exit(1)

    # Write the file to JSON.
    with open(ofile, "w+") as out:
        out.writelines(json.dumps(tree, indent=2))

def run_cli(with_args=None):
    """Start the main process for the CLI application.

    Arguments:
        with_Arguments: (Optional) The arguments to run the CLI with. Will default
        to sys.argv if no arguments have been supplied.
    """
    parser = _generate_args()
    args = []

    # Parse any arguments from the CLI when run.
    if sys.argv[1:]:
        args = parser.parse_args(with_args if with_args else sys.argv[1:])

    # Process the arguments if we have any.
    if args:
        # If the command is version, display the version and exit.
        if args.version:
            print("Efficacy CLI v0.1.0")
            return

        # If the input and token output are specified, run the token
        # generator.
        if args.input and args.output_tokens:
            for i, j in zip(args.input, args.output_tokens):
                _make_token_file(ifile=os.path.join(os.getcwd(), i),
                                 ofile=os.path.join(os.getcwd(), j))
            return

        # If the input and tree output are specified, run the parser
        # generator.
        if args.input and args.output_abstract_tree:
            for i, j in zip(args.input, args.output_abstract_tree):
                _make_parser_file(ifile=os.path.join(os.getcwd(), i),
                                  ofile=os.path.join(os.getcwd(), j))
            return

    # If no arguments have been supplied, run the interactive environment.
    else:
        print("Enter interactive mode here...")
