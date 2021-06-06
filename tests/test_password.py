# -*- coding: utf-8 -*-

"""
tests.test_password
===================

A testing module for `cues.password`.
"""

import pytest

from cues import cursor, password
from cues.password import Password


class TestPassword:
    def setup(self):
        self.name = 'password'
        self.message = 'Password:'
        self.message_endswith_alnum = 'Password'

    def test_init(self):
        cue = Password(self.name, self.message)

        assert cue._name == self.name
        assert cue._message == self.message

    def test_init_with_message_endswith_alnum(self):
        cue = Password(self.name, self.message_endswith_alnum)

        assert cue._name == self.name
        assert cue._message == self.message_endswith_alnum

    def test_send(self, monkeypatch):
        cue = Password(self.name, self.message)

        monkeypatch.setattr(cue, '_draw', lambda: None)
        assert cue.answer is None

    def test_draw(self, monkeypatch):
        cue = Password(self.name, self.message)
        up = cue.keys.get('up')
        down = cue.keys.get('down')
        right = cue.keys.get('right')
        left = cue.keys.get('left')
        enter = cue.keys.get('enter')
        backspace = cue.keys.get('backspace')

        def generic_return_none(*args, **kwargs):
            return None

        moves = [backspace, 49, 50, 51, 52, up, down, right, left, enter]

        def mock_listen_for_key():
            if moves:
                return moves.pop(0)

        monkeypatch.setattr(cursor, 'write', generic_return_none)
        monkeypatch.setattr(cue, 'listen_for_key', mock_listen_for_key)
        monkeypatch.setattr(cursor, 'move', generic_return_none)

        assert cue._draw() is None
        assert cue.answer == {self.name: '1234'}

    def test_from_dict(self):
        cue = Password(self.name, self.message)

        assert cue._name == self.name
        assert cue._message == self.message

    # For dev use only (do NOT use with CI):

    # def test__draw(self):
    #     print()
    #     cue = Password(self.name, self.message)

    #     answer = cue.send()
    #     print(answer)

    # def test__draw_message_endswith_alnum(self):
    #     print()
    #     cue = Password(self.name, self.message_endswith_alnum)

    #     answer = cue.send()
    #     print(answer)


def test_main(monkeypatch):
    monkeypatch.setattr(Password, 'send', lambda _: None)
    assert password.main() is None
