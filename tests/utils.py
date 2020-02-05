# -*- coding: utf-8 -*-
"""This submodule contains the component necessary to make a
printed test."""

import sys
from efficacy import __VERSION

def test(name):
    """A decorator used to classify a test case.

    Args:
        call: The function to be labeled as a test.
    """
    if not name:
        name = "sample"
    def func(call):
        def testfunc():
            if call and callable(call):
                try:
                    call()
                    print("✅  Test '%s' passed!" % (name))
                except Exception as err:
                    print("⛔️  Test failed with exception: " + str(err))
                    sys.exit(1)
        return testfunc
    return func

class TestError(Exception):
    """The base TestError case."""

@test
def test_version():
    """Test that the package version matches."""
    if __VERSION != "0.1.0":
        raise TestError("Version number doesn't match manifest.")
