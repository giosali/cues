"""
tests.test_confirm
==================

A testing module for `cues.confirm`.
"""

import pytest

from cues import confirm
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

    # For dev use only (do NOT use with CI):

    # def test__draw(self):
    #     cue = Confirm(self.name, self.message)

    #     print()
    #     answer = cue.send()
    #     print()
    #     print(f'My answer: {answer}')


def test_main():
    assert confirm.main(1) == None
