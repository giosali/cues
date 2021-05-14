"""
tests.test_cues
===============

A testing module for `cues.cues`.
"""

import copy

import pytest

from cues import constants
from cues.cues import Select, Confirm, Form, Survey


class TestSelect:
    def setup(self):
        self.name = 'programming_language'
        self.message = 'Select a programming language:'
        self.options = [
            'Python',
            'JavaScript',
            'C++',
        ]

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


class TestConfirm:
    def setup(self):
        self.name = 'continue'
        self.message = 'Are you sure you would like to continue?'

    def test__init__(self):
        cue = Confirm(self.name, self.message)

        assert cue._name == self.name
        assert cue._message == self.message

    def test__init__errors(self):
        with pytest.raises(TypeError):
            Confirm(1, self.message)
        with pytest.raises(TypeError):
            Confirm(self.name, 1)

    # For dev use only (do NOT use with CI):

    # def test__draw(self):
    #     cue = Confirm(self.name, self.message)

    #     print()
    #     answer = cue.send()
    #     print()
    #     print(f'My answer: {answer}')


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

    # For dev use only (do NOT use with CI):

    # def test__draw(self):
    #     print()
    #     cue = Form(self.name, self.message, self.fields)

    #     answer = cue.send()
    #     print(answer)


class TestSurvey:
    def setup(self):
        self.name = 'customer_satisfaction'
        self.message = 'Please rate the following areas:'
        # self.scale = [
        #     'Very dissatisfied',
        #     'Dissatisfied',
        #     'Neutral',
        #     'Satisfied',
        #     'Very satisfied'
        # ]
        self.scale = [
            1,
            2,
            3,
            4,
            5
        ]
        self.fields = [
            {
                'name': 'customer_service',
                'message': 'Customer service'
            },
            {
                'name': 'restaurant_service',
                'message': 'Restaurant service'
            },
            {
                'name': 'bar_service',
                'message': 'Bar service'
            },
            {
                'name': 'room_service',
                'message': 'Room service'
            }
        ]

    def test__init__(self):
        cue = Survey(self.name, self.message, self.scale, self.fields)

        assert cue._name == self.name
        assert cue._message == self.message

        assert cue._scale == self.scale
        assert cue._fields == self.fields

    def test__init__errors(self):
        with pytest.raises(TypeError):
            Survey(1, self.message, self.scale, self.fields)
        with pytest.raises(TypeError):
            Survey(self.name, 1, self.scale, self.fields)
        with pytest.raises(TypeError):
            Survey(self.name, self.message, 1, self.fields)
        with pytest.raises(TypeError):
            Survey(self.name, self.message, self.scale, 1)

    # For dev use only (do NOT use with CI):

    # def test__draw(self):
    #     cue = Survey(self.name, self.message, self.scale, self.fields)

    #     answer = cue.send()
    #     print(answer)
