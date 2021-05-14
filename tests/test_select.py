"""
tests.test_select
==============

A testing module for `cues.select`.
"""

import pytest

from cues import select


def test_main():
    assert select.main(1) == None
