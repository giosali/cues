"""
tests.test_form
===============

A testing module for `cues.form`.
"""

import pytest

from cues import form
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

    def test__init__(self):
        cue = Form(self.name, self.message, self.fields)

        assert cue._name == self.name
        assert cue._message == self.message

        assert cue._fields == self.fields

    def test__init__errors(self):
        with pytest.raises(TypeError):
            Form(1, self.message, self.fields)
        with pytest.raises(TypeError):
            Form(self.name, 1, self.fields)
        with pytest.raises(TypeError):
            Form(self.name, self.message, 1)

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


def test_main():
    assert form.main(1) == None
