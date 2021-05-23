"""
tests.test_cursor
=================

A testing module for `cues.cursor`.
"""

import pytest

from cues import cursor


def test_show():
    assert cursor.show() == None


def test_hide():
    assert cursor.hide() == None


def test_clear():
    lines = 2

    assert cursor.clear(lines) == None


def test_move_up_and_right():
    x = 2
    y = 1

    assert cursor.move(x, y) == None


def test_move_down_and_left():
    x = -2
    y = -1

    assert cursor.move(x, y) == None


def test_write():
    text = 'text'

    assert cursor.write(text) == None


def test_write_with_color():
    text = 'text'

    assert cursor.write(text, color=True) == None


def test_write_with_newlines():
    text = 'text'

    assert cursor.write(text, newlines=1) == None
