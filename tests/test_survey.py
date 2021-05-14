"""
tests.test_survey
==============

A testing module for `cues.survey`.
"""

import pytest

from cues import survey


def test_main():
    assert survey.main(1) == None
