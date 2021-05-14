"""
tests.test_form
===============

A testing module for `cues.form`.
"""

import pytest

from cues import form


def test_main():
    assert form.main(1) == None
