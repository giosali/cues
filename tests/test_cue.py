"""
tests.test_cue
==============

A testing module for `cues.cue`.
"""

import sys
from abc import ABCMeta
from collections import deque
from dataclasses import dataclass

import pytest

from cues.cue import Cue


@pytest.mark.skipif(sys.version_info < (3, 7), reason='requires Python 3.7 or higher')
def test_cue():
    Cue.__abstractmethods__ = set()

    assert isinstance(Cue, ABCMeta)

    @dataclass
    class DummyCue(Cue):
        pass

    dc = DummyCue()

    # properties:

    name = 'name'
    response = 'answer'
    answer = {name: response}
    dc.answer = answer
    assert dc.answer == answer

    # abstractmethods:

    assert dc.send() == None
    assert dc._draw() == None

    # staticmethods:

    dummy_list_with_int = [1, 2, 3]
    dummy_list_with_int_to_str = [str(i) for i in dummy_list_with_int]
    assert dc.create_deque(dummy_list_with_int) == deque(
        dummy_list_with_int_to_str)

    dummy_list_with_str = ['a', 'b', 'c', 'd']
    assert dc.create_deque(dummy_list_with_str) == deque(dummy_list_with_str)

    assert not dc.create_deque([])
