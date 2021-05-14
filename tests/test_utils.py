"""
tests.test_utils
================

A testing module for `cues.utils`.
"""

import math
import platform

import pytest

import cues.utils as utils


def test_is_windows():
    system = platform.system()

    if system == 'Windows':
        assert utils.is_windows()
    else:
        assert not utils.is_windows()


def test_get_keys():
    keys = utils.get_keys()

    assert isinstance(keys, dict)
    assert len(keys) >= 4


def test_get_num_digits():
    number = 2345
    num_digits = 4

    assert utils.get_num_digits(number) == num_digits


def test_get_half():
    number = 23
    expected_result = math.ceil(number / 2)

    assert utils.get_half(number) == expected_result
