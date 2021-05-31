"""
tests.test_checkbox
===================

A testing module for `cues.checkbox`.
"""

import pytest

from cues import checkbox, cursor
from cues.checkbox import Checkbox


class TestCheckbox:
    def setup(self):
        self.name = 'guitars'
        self.message = 'Pick your favorite guitars:'
        self.options = [
            'Les Paul',
            'Stratocaster',
            'Telecaster',
            'SG',
            'Flying V',
            'Acoustic',
            'Classical',
        ]

    def test_init(self):
        cue = Checkbox(self.name, self.message, self.options)

        assert cue._name == self.name
        assert cue._message == self.message
        assert cue._options == self.options

    def test_init_errors(self):
        bad_options = 1

        with pytest.raises(TypeError):
            cue = Checkbox(self.name, self.message, bad_options)

    def test_send(self, monkeypatch):
        cue = Checkbox(self.name, self.message, self.options)

        monkeypatch.setattr(cursor, 'hide', lambda: None)
        monkeypatch.setattr(cursor, 'show', lambda: None)
        monkeypatch.setattr(cue, '_draw', lambda: None)

        cue.send()
        assert cue.answer is None

    def test_draw_with_up_and_down_keys(self, monkeypatch):
        cue = Checkbox(self.name, self.message, self.options)
        up = cue.keys.get('up')
        down = cue.keys.get('down')
        enter = cue.keys.get('enter')

        moves = [up, down, up, down, down, down, down, down, down, down]

        def mock_listen_for_key():
            if moves:
                return moves.pop(0)
            return enter

        monkeypatch.setattr(cursor, 'write', lambda _,
                            color=True, newlines=1: None)
        monkeypatch.setattr(cue, 'listen_for_key', mock_listen_for_key)
        monkeypatch.setattr(cursor, 'clear', lambda _: None)

        assert cue._draw() is None
        assert cue.answer == {self.name: []}

    def test_draw_with_space_key(self, monkeypatch):
        cue = Checkbox(self.name, self.message, self.options)
        space = cue.keys.get('space')
        enter = cue.keys.get('enter')

        moves = [space, space]

        def mock_listen_for_key():
            if moves:
                return moves.pop(0)
            return enter

        monkeypatch.setattr(cursor, 'write', lambda _,
                            color=True, newlines=1: None)
        monkeypatch.setattr(cue, 'listen_for_key', mock_listen_for_key)
        monkeypatch.setattr(cursor, 'clear', lambda _: None)

        assert cue._draw() is None
        assert cue.answer == {self.name: []}

    def test_draw_with_enter_key(self, monkeypatch):
        cue = Checkbox(self.name, self.message, self.options)
        enter = cue.keys.get('enter')

        monkeypatch.setattr(cursor, 'write', lambda _,
                            color=True, newlines=1: None)
        monkeypatch.setattr(cue, 'listen_for_key', lambda: enter)
        monkeypatch.setattr(cursor, 'clear', lambda _: None)

        assert cue._draw() is None
        assert cue.answer == {self.name: []}

    def test_from_dict(self):
        checkbox_dict = {
            'name': self.name,
            'message': self.message,
            'options': self.options
        }
        cue = Checkbox.from_dict(checkbox_dict)

        assert cue._name == self.name
        assert cue._message == self.message
        assert cue._options == self.options

    # For dev use only (do NOT use with CI):

    # def test_draw(self):
    #     cue = Checkbox(self.name, self.message, self.options)

    #     print()
    #     answer = cue.send()
    #     print(answer)


def test_main(monkeypatch):
    monkeypatch.setattr(Checkbox, 'send', lambda _: None)
    assert checkbox.main() is None
