# -*- coding: utf-8 -*-

"""
cues.survey
===========

A module that contains the Survey class.
"""

import copy
from typing import Iterable

from . import constants, cursor, utils
from .cue import Cue


class Survey(Cue):
    """Construct a Survey object to retrieve one or more responses from a user.

    A Survey object will display a sequence of questions to the user
    and ask the user to answer them by using a scale. The user can
    use the Right and Left arrow keys to select an option on the scale
    and press Enter to move to the next question.

    Attributes
    ----------
    _scale : list
        The range of the scale.
    _fields : list
        Contains dicts (fields) to construct a survey.
    _legend : list
        Contains strings that define values for _scale.
    _legend_fmt : str
        The format for the legend.
    _header_fmt : str
        The format for the legend header.
    _space_btwn : int
        Constant integer representing the space between legend values.
        This is only used if there are only two legend values.
    _total_legend_fmt_len : int
        Represents the total space between the header.
        This is only used if there are only two legend values.
    _init_fmt : str
        The format for the initial statement.
    _msg_fmt : str
        The format for the message.
    _pt_fmt : str
        The format for the number of points in the scale.
    _scale_fmt : str
        The format for the values of the scale.
    """

    __name__ = 'Survey'
    __module__ = 'cues'

    def __init__(self, name: str, message: str, scale: Iterable,
                 fields: Iterable[dict], legend: Iterable = []):
        """

        Parameters
        ----------
        name
            The name of the Survey instance.
        message
            Instructions or useful information regarding the prompt for the user.
        scale
            The range of the scale.
        fields
            Contains questions/information for the user to respond to.
        legend : iterable, optional
            Defines the values of the scale.
        """

        super().__init__(name, message)

        if hasattr(scale, '__iter__'):
            self._scale = list(scale)
        else:
            raise TypeError(f"'{type(scale)}' object is not iterable")

        if hasattr(fields, '__iter__'):
            self._fields = list(fields)
        else:
            raise TypeError(f"'{type(fields)}' object is not iterable")

        try:
            self._legend = list(scale.values())
        except (NameError, AttributeError):
            self._legend = legend

        if self._legend:
            legend_len = len(self._legend)
            scale_len = len(self._scale)

            if legend_len == scale_len:
                self._legend_fmt = '\t[grey]{val} : {legend}[/grey]\n'
                self._header_fmt = None

            elif legend_len == 2:
                legend_fmt = '\t[grey]{:<{space}}[/grey]' * scale_len
                max_legend_len, index = utils.get_max_len(self._legend)

                tab = 4
                max_legend_len -= (0 if max_legend_len <= tab else tab)

                self._space_btwn = 6
                self._total_legend_fmt_len = self._space_btwn * scale_len + 1
                self._legend_fmt = (max_legend_len * ' ') + legend_fmt

                self._header_fmt = (' ' * (tab if index else 0)
                                    ) + '[grey]{}{space}{}[/grey]'
        else:
            self._legend_fmt = None
            self._header_fmt = None
            self._space_btwn = None
            self._total_legend_fmt_len = None

        self._init_fmt = '[pink][?][/pink] {msg}\n\n'

        self._msg_fmt = '{count}. {msg}\n'  # Top

        lines_and_pts = '{line}'.join(['{}' for _ in range(len(self._scale))])
        self._pt_fmt = '[skyblue]' + lines_and_pts + '[/skyblue]\n'  # Middle

        self._scale_fmt = '{:<{length}}'  # Bottom

    def send(self):
        """Returns a dict object containing user's response to the prompt.

        Returns
        -------
        dict
            A dict containing the user's response to the prompt.
        """

        try:
            cursor.hide()

            self._draw()
            return self.answer
        finally:
            cursor.show()

    def _draw(self):
        """Prints the prompt to console and sets user's response.
        """

        cursor.write(self._init_fmt.format(msg=self._message), color=True)

        if self._legend:
            # If there are only two elems in self._legend:
            if self._header_fmt:
                cursor.write(self._header_fmt.format(
                    *self._legend, space=self._total_legend_fmt_len * ' '), color=True, newlines=1)
                cursor.write(self._legend_fmt.format(
                    *self._scale, space=self._space_btwn), color=True, newlines=3)
            # else, if lengths of _legend and _scale are equal:
            else:
                for pt, desc in zip(self._scale, self._legend):
                    cursor.write(self._legend_fmt.format(
                        val=pt, legend=desc), color=True)
                cursor.write('', newlines=2)

        # For keeping track of location:
        scale_len = len(self._scale)
        max_fields = len(self._fields) * 4
        current_field = max_fields

        # Creates line between survey points:
        deque_scale = self.create_deque(self._scale)
        current_deque_scale = copy.copy(deque_scale)

        center_pt = utils.get_half(scale_len)
        pts = [constants.SURVEY_PT for _ in range(scale_len)]
        pts[center_pt - 1] = constants.SURVEY_PT_FILL
        deque_pts = self.create_deque(pts)
        current_deque_pts = copy.copy(deque_pts)

        min_space_btwn_lines = 5
        max_line_len = max(
            len(elem) for elem in deque_scale) + min_space_btwn_lines
        line = constants.SURVEY_LINE * max_line_len

        scale_str = ''
        for val in deque_scale:
            scale_str += self._scale_fmt.format(val, length=max_line_len + 1)
        scale_str += '\n'

        messages = [field['message'] for field in self._fields]

        default_margin = 2

        for c, message in enumerate(messages, 1):
            cursor.write(self._msg_fmt.format(count=c, msg=message))

            # Adds space in front:
            margin = ' ' * (default_margin + utils.get_num_digits(c))

            cursor.write(
                margin + self._pt_fmt.format(*deque_pts, line=line), color=True)
            cursor.write(margin + scale_str + '\n')

        cursor.move(y=current_field)

        right = self.keys.get('right')
        left = self.keys.get('left')
        enter = self.keys.get('enter')

        horziontal_num = center_pt
        current_val = 0

        responses = {}

        # Actual drawing:
        while True:
            cursor.write(self._msg_fmt.format(
                count=current_val + 1, msg=messages[current_val]))

            # Adds space in front:
            margin = ' ' * (default_margin +
                            utils.get_num_digits(current_val + 1))

            cursor.write(
                margin + self._pt_fmt.format(*current_deque_pts, line=line), color=True)

            scale_str = ''
            for c, val in enumerate(current_deque_scale, 1):
                temp_line_len = 0
                if c == horziontal_num:
                    val = '[underline lightslateblue]' + \
                        val + '[/underline lightslateblue]'
                    temp_line_len = max_line_len + len(val)
                scale_str += self._scale_fmt.format(
                    val, length=(temp_line_len or max_line_len + 1))
            scale_str += '\n'
            cursor.write(margin + scale_str + '\n', color=True)

            cursor.move(y=-(current_field - 4))

            key = self.listen_for_key()

            if key == right:
                # If cursor is at very right:
                if current_deque_pts[-1] == constants.SURVEY_PT_FILL:
                    pass
                else:
                    current_deque_pts.appendleft(constants.SURVEY_PT)
                    horziontal_num += 1

            elif key == left:
                # If cursor is at very left:
                if current_deque_pts[0] == constants.SURVEY_PT_FILL:
                    pass
                else:
                    current_deque_pts.append(constants.SURVEY_PT)
                    horziontal_num -= 1

            elif key == enter:
                # Add current scale value to dict
                responses.update({
                    self._fields[current_val]['name']: self._scale[horziontal_num - 1]})
                current_val += 1

                # If at the end of the survey, then quit:
                if current_val == scale_len - 1:
                    if self._header_fmt:
                        cursor.clear(max_fields + 4)
                    else:
                        cursor.clear(
                            max_fields + (len(self._legend) + 2 if self._legend else 0))

                    break
                else:
                    current_field -= 4
                    # Resets values:
                    current_deque_pts = copy.copy(deque_pts)
                    current_deque_scale = copy.copy(deque_scale)
                    horziontal_num = center_pt

            # Resets cursor at top:
            cursor.move(y=current_field)

        self.answer = {self._name: responses}

    @classmethod
    def from_dict(cls, prompt: dict):
        """Creates and instantiates a Survey object from a dict object.

        Parameters
        ----------
        prompt : dict
            A dict object that contains a name key, a message key, a
            scale key, a fields key, and an optional legend key.

        Returns
        -------
        cues.Survey
            A Survey object to retrieve a single response from a user.
        """

        name = prompt['name']
        message = prompt['message']
        scale = prompt['scale']
        fields = prompt['fields']
        legend = prompt.get('legend', [])
        return cls(name, message, scale, fields, legend)


def main(test=0):
    name = 'customer_satisfaction'
    message = 'Please rate your satisfaction with the following areas:'
    scale = [1, 2, 3, 4, 5]
    fields = [
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

    prompt = Survey(name, message, scale, fields)
    answer = prompt.send()
    print(answer)


if __name__ == '__main__':  # pragma: no cover
    main()
