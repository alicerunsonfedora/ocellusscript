"""This submodule contains the component necessary to make a
printed test."""

from efficacy import __VERSION

def test(call):
    """A decorator used to classify a test case.

    Args:
        call: The function to be labeled as a test.
    """
    def testfunc():
        if call and callable(call):
            try:
                call()
                print("✅  Test passed!")
            except Exception as err:
                print("⛔️  Test failed with exception " + err)
    return testfunc

class TestError(Exception):
    """The base TestError case."""

@test
def test_version():
    """Test that the package version matches."""
    if __VERSION != "0.1.0":
        raise TestError("Version number doesn't match manifest.")