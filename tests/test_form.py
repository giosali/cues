"""
tests.test_form
===============

A testing module for `cues.form`.
"""

import pytest

from cues import form, cursor
from cues.form import Form


class TestForm:
    def setup(self):
        self.name = 'basic_info'
        self.message = 'Please fill out the following form:'
        self.fields = [
            {
                'name': 'first_name',
                'message': 'What is your first name?',
                'default': 'Giovanni'
            },
            {
                'name': 'last_name',
                'message': 'What is your last name?',
                'default': 'Salinas'
            },
            {
                'name': 'language',
                'message': 'What is your favorite programming language?',
                'default': 'Python'
            }
        ]

        self.dic = {
            'name': self.name,
            'message': self.message,
            'fields': self.fields
        }

    def test_init(self):
        cue = Form(self.name, self.message, self.fields)

        assert cue._name == self.name
        assert cue._message == self.message

        assert cue._fields == self.fields

    def test_init_errors(self):
        with pytest.raises(TypeError):
            Form(1, self.message, self.fields)
        with pytest.raises(TypeError):
            Form(self.name, 1, self.fields)
        with pytest.raises(TypeError):
            Form(self.name, self.message, 1)

    def test_send(self, monkeypatch):
        cue = Form(self.name, self.message, self.fields)

        monkeypatch.setattr(cue, '_draw', lambda: None)
        assert cue.answer is None

    def test_draw(self, monkeypatch):
        cue = Form(self.name, self.message, self.fields)
        up = cue.keys.get('up')
        down = cue.keys.get('down')
        left = cue.keys.get('left')
        right = cue.keys.get('right')
        backspace = cue.keys.get('backspace')
        enter = cue.keys.get('enter')
        ordinal = 71

        def mock_move(*args, **kwargs):
            return None

        moves = [ordinal, down, up, left, right,
                 backspace, enter, enter, enter]

        def mock_listen_for_key():
            if moves:
                return moves.pop(0)

        monkeypatch.setattr(cursor, 'write', lambda _, color=True: None)
        # monkeypatch.setattr(cue, '__print_fields',
        #                     lambda _, __, ___, ____: None)
        monkeypatch.setattr(cursor, 'move', mock_move)
        monkeypatch.setattr(cue, 'listen_for_key', mock_listen_for_key)
        monkeypatch.setattr(cursor, 'clear', lambda _: None)

        cue._draw()
        fields_dict = {}
        for field in self.fields:
            fields_dict.update({field['name']: field.get('default', '')})
        expected_answer = {self.name: fields_dict}
        assert cue.answer == expected_answer

    def test_from_dict(self):
        cue = Form.from_dict(self.dic)

        assert cue._name == self.name
        assert cue._message == self.message

        assert cue._fields == self.fields

    # For dev use only (do NOT use with CI):

    # def test__draw(self):
    #     print()
    #     cue = Form(self.name, self.message, self.fields)

    #     answer = cue.send()
    #     print(answer)


def test_main(monkeypatch):
    monkeypatch.setattr(Form, 'send', lambda _: None)
    assert form.main() is None
