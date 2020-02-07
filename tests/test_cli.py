"""This module contains the CLI tests for Efficacy.

The following test functions are provided to test that the CLI
application works as intended.
"""

#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

import json
import os
from efficacy.cli import run_cli

def test_write_tokens():
    """Test that the token writing functionality works as intended."""
    current_tokens = []
    expected_tokens = []

    if "tmp" in os.listdir(os.getcwd()):
        for file in os.listdir("tmp"):
            os.remove("tmp/" + file)
        os.rmdir("tmp")

    os.mkdir("tmp")

    with open("tmp/sample.ocls", "w+") as sample:
        sample.write("example t = t > 6.0 ? t + 5.3 : t")
    run_cli(["-i", "tmp/sample.ocls", "-oT", "tmp/basic.json"])

    with open("tmp/basic.json", "r") as curr:
        current_tokens = json.loads(curr.read())

    for file in os.listdir("tmp"):
        os.remove("tmp/" + file)
    os.rmdir("tmp")

    with open("tests/data/basic.json") as expec:
        expected_tokens = json.loads(expec.read())
    assert current_tokens == expected_tokens
