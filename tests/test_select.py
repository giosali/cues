"""
tests.test_select
=================

A testing module for `cues.select`.
"""

import copy

import pytest

from cues import select
from cues.select import Select


class TestSelect:
    def setup(self):
        self.name = 'programming_language'
        self.message = 'Select a programming language:'
        self.options = [
            'Python',
            'JavaScript',
            'C++',
        ]

        self.dic = {
            'name': self.name,
            'message': self.message,
            'options': self.options
        }

    def test__init__(self):
        cue = Select(self.name, self.message, self.options)

        # ABC:
        assert cue._name == self.name
        assert cue._message == self.message

        assert cue._options == self.options
        assert cue._num_options == len(self.options)

        # Property methods:
        assert cue.markers == cue._markers

    def test__init__errors(self):
        with pytest.raises(TypeError):
            Select(1, self.message, self.options)
        with pytest.raises(TypeError):
            Select(self.name, 1, self.options)
        with pytest.raises(TypeError):
            Select(self.name, self.message, 1)

    def test_from_dict(self):
        cue = Select.from_dict(self.dic)

        # ABC:
        assert cue._name == self.name
        assert cue._message == self.message

        assert cue._options == self.options
        assert cue._num_options == len(self.options)

        # Property methods:
        assert cue.markers == cue._markers

    def test_options_property(self):
        cue = Select(self.name, self.message, self.options)

        # Getter:

        assert cue.options == self.options
        assert len(cue.options) == cue._num_options

    def test_markers_property(self):
        cue = Select(self.name, self.message, self.options)

        # Getter:

        assert cue.markers == cue._markers
        assert len(cue.markers) == len(cue._markers)

        # Setter:

        shallow_copy_markers = copy.copy(cue.markers)  # ['>', ' ', ' ']

        # -- If up arrow key is pressed:

        cue.markers = 1  # Marker moved up: [' ', ' ', '>']
        assert cue.markers == cue._markers
        assert len(cue.markers) == cue._num_options
        assert cue.markers != shallow_copy_markers

        cue.markers = 1  # Marker moved up: [' ', '>', ' ']
        assert cue.markers == cue._markers
        assert len(cue.markers) == cue._num_options
        assert cue.markers != shallow_copy_markers

        cue.markers = 1  # Marker moved up: ['>', ' ', ' ']
        assert cue.markers == cue._markers
        assert len(cue.markers) == cue._num_options
        assert cue.markers == shallow_copy_markers

        # -- If down arrow key is pressed:

        cue.markers = 0  # Marker moved down: [' ', '>', ' ']
        assert cue.markers == cue._markers
        assert len(cue.markers) == cue._num_options
        assert cue.markers != shallow_copy_markers

        cue.markers = 0  # Marker moved down: [' ', ' ', '>']
        assert cue.markers == cue._markers
        assert len(cue.markers) == cue._num_options
        assert cue.markers != shallow_copy_markers

        cue.markers = 0  # Marker moved down: ['>', ' ', ' ']
        assert cue.markers == cue._markers
        assert len(cue.markers) == cue._num_options
        assert cue.markers == shallow_copy_markers

    # For dev use only (do NOT use with CI):

    # def test__draw(self):
    #     cue = Select(self.name, self.message, self.options)
    #     print()
    #     answer = cue.send()
    #     print(answer)


def test_main():
    assert select.main(1) == None
