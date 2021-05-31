"""
tests.test_confirm
==================

A testing module for `cues.confirm`.
"""

import pytest

from cues import confirm, cursor
from cues.confirm import Confirm


class TestConfirm:
    def setup(self):
        self.name = 'continue'
        self.message = 'Are you sure you would like to continue?'

        self.dic = {
            'name': self.name,
            'message': self.message
        }

    def test__init__(self):
        cue = Confirm(self.name, self.message)

        assert cue._name == self.name
        assert cue._message == self.message

    def test__init__errors(self):
        with pytest.raises(TypeError):
            Confirm(1, self.message)
        with pytest.raises(TypeError):
            Confirm(self.name, 1)

    def test_from_dict(self):
        cue = Confirm.from_dict(self.dic)

        assert cue._name == self.name
        assert cue._message == self.message

    def test_send(self, monkeypatch):
        cue = Confirm(self.name, self.message)

        monkeypatch.setattr(cursor, 'hide', lambda: None)
        monkeypatch.setattr(cursor, 'show', lambda: None)
        monkeypatch.setattr(cue, '_draw', lambda: None)

        cue.send()

        assert cue.answer is None

    def test_draw_with_y(self, monkeypatch):
        cue = Confirm(self.name, self.message)

        monkeypatch.setattr(cue, 'listen_for_key', lambda: cue.keys.get('y'))
        monkeypatch.setattr(cursor, 'write', lambda _, color=True: None)

        cue._draw()

        assert cue.answer == {self.name: True}

    def test_draw_with_n(self, monkeypatch):
        cue = Confirm(self.name, self.message)

        monkeypatch.setattr(cue, 'listen_for_key', lambda: cue.keys.get('n'))
        monkeypatch.setattr(cursor, 'write', lambda _, color=True: None)

        cue._draw()

        assert cue.answer == {self.name: False}

    # For dev use only (do NOT use with CI):

    # def test__draw(self):
    #     cue = Confirm(self.name, self.message)

    #     print()
    #     answer = cue.send()
    #     print()
    #     print(f'My answer: {answer}')


def test_main(monkeypatch):
    monkeypatch.setattr(Confirm, 'send', lambda _: None)
    assert confirm.main() is None
