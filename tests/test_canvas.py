# -*- coding: utf-8 -*-

"""
tests.test_canvas
=================

A testing module for `cues.canvas`.
"""

import sys
from abc import ABCMeta
try:
    from dataclasses import dataclass
except ModuleNotFoundError:
    pass

import pytest

from cues.canvas import Canvas


@pytest.mark.skipif(sys.version_info < (3, 7), reason='requires Python 3.7 or higher')
def test_canvas():
    Canvas.__abstractmethods__ = set()

    assert isinstance(Canvas, ABCMeta)

    @dataclass
    class DummyCanvas(Canvas):
        pass

    dc = DummyCanvas()

    # Methods

    assert dc.update_cursor_position() == None
    assert dc.update_max_columns() == None

    # Context manager

    with DummyCanvas() as dc2:
        assert isinstance(dc2, DummyCanvas)
