"""This module contains important tests for package metadata."""
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from efficacy import __VERSION

def test_version():
    """Verify that the version number matches what we currently have."""
    assert __VERSION == "0.1.0"
