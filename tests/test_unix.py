"""
tests.test_unix
===============

A testing module for `cues.listen.unix`.
"""

import platform

from cues.listen import unix


def test_is_data():
    if platform.system() != 'Windows':
        assert not unix.is_data()
