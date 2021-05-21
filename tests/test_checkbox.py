"""
tests.test_checkbox
===================

A testing module for `cues.checkbox`.
"""

import pytest

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
