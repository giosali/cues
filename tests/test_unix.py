# -*- coding: utf-8 -*-

"""
tests.test_unix
===============

A testing module for `cues.listen.unix`.
"""

import platform
import select
import sys
try:
    import termios  # pylint: disable=import-error
except ModuleNotFoundError:
    pass
try:
    import tty
except ModuleNotFoundError:
    pass

import pytest

import cues.listen.unix as unix


@pytest.mark.skipif(platform.system() == 'Windows', reason='OS must not be Windows')
def test_listen(monkeypatch):
    character = 'a'

    def mock_read_return(_):
        return character

    monkeypatch.setattr(sys.stdin, 'fileno', lambda: None)
    monkeypatch.setattr(termios, 'tcgetattr', lambda _: 0)
    monkeypatch.setattr(tty, 'setcbreak', lambda _: None)
    monkeypatch.setattr(unix, 'is_data', lambda: True)
    monkeypatch.setattr(sys.stdin, 'read', mock_read_return)
    monkeypatch.setattr(termios, 'tcsetattr', lambda _, __, ___: 0)

    x = unix.listen()
    assert x == ord(character)


@pytest.mark.skipif(platform.system() == 'Windows', reason='OS must not be Windows')
def test_get_key(monkeypatch):
    character = 'a'

    def mock_read_return(_):
        return character

    monkeypatch.setattr(unix, 'is_data', lambda: True)
    monkeypatch.setattr(sys.stdin, 'read', mock_read_return)

    x = unix.get_key()
    assert x == ord(character)


@pytest.mark.skipif(platform.system() == 'Windows', reason='OS must not be Windows')
def test_get_key_when_key_is_esc(monkeypatch):
    character = '\x1b'

    def mock_read_return(_):
        return character

    monkeypatch.setattr(unix, 'is_data', lambda: True)
    monkeypatch.setattr(sys.stdin, 'read', mock_read_return)

    x = unix.get_key()
    assert x == character


@pytest.mark.skipif(platform.system() == 'Windows', reason='OS must not be Windows')
def test_is_data(monkeypatch):
    monkeypatch.setattr(sys.stdin, 'fileno', lambda: None)
    monkeypatch.setattr(select, 'select', lambda _, __, ___, ____: True)

    x = unix.is_data()
    assert x is False


@pytest.mark.skipif(platform.system() == 'Windows', reason='OS must not be Windows')
def test_listen_for_pos(monkeypatch):
    def generic_return_none(*args, **kwargs):
        return None

    def mock_read_return():
        nums = [10, 6]
        pos = '\x1b[{};{}R'.format(*nums)
        return pos

    monkeypatch.setattr(sys.stdin, 'fileno', generic_return_none)
    monkeypatch.setattr(termios, 'tcgetattr', lambda _: 0)
    monkeypatch.setattr(tty, 'setcbreak', generic_return_none)
    monkeypatch.setattr(unix, 'get_pos', mock_read_return)
    monkeypatch.setattr(termios, 'tcsetattr', lambda _, __, ___: 0)

    assert unix.listen_for_pos() == '\x1b[10;6R'


@pytest.mark.skipif(platform.system() == 'Windows', reason='OS must not be Windows')
def test_get_pos(monkeypatch):
    def generic_return_none(*args, **kwargs):
        return None

    def mock_read_return(_):
        nums = [10, 6]
        pos = '\x1b[{};{}R'.format(*nums)
        return pos

    monkeypatch.setattr(sys.stdout, 'write', generic_return_none)
    monkeypatch.setattr(sys.stdout, 'flush', generic_return_none)
    monkeypatch.setattr(sys.stdin, 'read', mock_read_return)

    assert unix.get_pos() == '\x1b[10;6R'
