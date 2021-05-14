"""
tests.test_confirm
==================

A testing module for `cues.confirm`.
"""

import pytest

from cues import confirm


def test_main():
    assert confirm.main(1) == None
