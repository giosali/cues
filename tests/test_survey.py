"""
tests.test_survey
=================

A testing module for `cues.survey`.
"""

import pytest

from cues import survey
from cues.survey import Survey


class TestSurvey:
    def setup(self):
        self.name = 'customer_satisfaction'
        self.message = 'Please rate the following areas:'
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

        self.scale_with_equal_descs = {
            1: 'Very poor',
            2: 'Poor',
            3: 'Average',
            4: 'Good',
            5: 'Very good'
        }

        self.legend = [
            'Very poor',
            'Poor',
            'Average',
            'Good',
            'Very good'
        ]
        self.legend_two = [
            'Very dissatisfied',
            'Very satisfied'
        ]
        # self.legend_two = [
        #     'dissatisfied',
        #     'Very satisfied'
        # ]

        self.dic = {
            'name': self.name,
            'message': self.message,
            'scale': self.scale,
            'fields': self.fields
        }

    def test__init__(self):
        cue = Survey(self.name, self.message, self.scale, self.fields)

        assert cue._name == self.name
        assert cue._message == self.message

        assert cue._scale == self.scale
        assert cue._fields == self.fields

    def test__init__with_scale_with_equal_descs(self):
        cue = Survey(self.name, self.message,
                     self.scale_with_equal_descs, self.fields)

        assert cue._name == self.name
        assert cue._message == self.message

        assert cue._scale == list(self.scale_with_equal_descs)
        assert cue._fields == self.fields
        assert cue._legend == list(self.scale_with_equal_descs.values())

    def test__init__with_legend(self):
        cue = Survey(self.name, self.message, self.scale,
                     self.fields, self.legend)

        assert cue._name == self.name
        assert cue._message == self.message

        assert cue._scale == self.scale
        assert cue._fields == self.fields
        assert cue._legend == self.legend

    def test__init__with_legend_two(self):
        cue = Survey(self.name, self.message, self.scale,
                     self.fields, self.legend_two)

        assert cue._name == self.name
        assert cue._message == self.message

        assert cue._scale == self.scale
        assert cue._fields == self.fields
        assert cue._legend == self.legend_two

    def test__init__errors(self):
        with pytest.raises(TypeError):
            Survey(1, self.message, self.scale, self.fields)
        with pytest.raises(TypeError):
            Survey(self.name, 1, self.scale, self.fields)
        with pytest.raises(TypeError):
            Survey(self.name, self.message, 1, self.fields)
        with pytest.raises(TypeError):
            Survey(self.name, self.message, self.scale, 1)

    def test_from_dict(self):
        cue = Survey.from_dict(self.dic)

        assert cue._name == self.name
        assert cue._message == self.message

        assert cue._scale == self.scale
        assert cue._fields == self.fields

    # For dev use only (do NOT use with CI):

    # def test__draw(self):
    #     cue = Survey(self.name, self.message, self.scale, self.fields)

    #     print()
    #     answer = cue.send()
    #     print(answer)

    # def test__draw_with_legend(self):
    #     cue = Survey(self.name, self.message, self.scale,
    #                  self.fields, self.legend)

    #     print()
    #     answer = cue.send()
    #     print(answer)

    # def test__draw_with_legend_two(self):
    #     cue = Survey(self.name, self.message, self.scale,
    #                  self.fields, self.legend_two)

    #     print()
    #     answer = cue.send()
    #     print(answer)

    # def test__draw_with_scale_with_equal_descs(self):
    #     cue = Survey(self.name, self.message,
    #                  self.scale_with_equal_descs, self.fields)

    #     print()
    #     answer = cue.send()
    #     print(answer)


def test_main():
    assert survey.main(1) == None
