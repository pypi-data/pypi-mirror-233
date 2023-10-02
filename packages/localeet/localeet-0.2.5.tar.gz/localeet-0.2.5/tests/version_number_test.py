"""
Tests that version number has increased from PyPI-deployed version.
"""

from localeet.get_version import get_version

from conftest import MockValue


def test_get_version(any_version: MockValue) -> None:
    assert get_version() == any_version
