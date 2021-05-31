# -*- coding: utf-8 -*-

"""
cues.form
=========

This module contains the Form class.
"""

from typing import Iterable

from . import constants, cursor, utils
from .cue import Cue


class Form(Cue):
    """Construct a Form object to retrieve several responses from a user.

    Form objects can be used to display a form-like prompt to the 
    user and ask the user to answer corresponding questions. The user 
    can type their answers and use the up and down arrow keys and the 
    ENTER key to navigate the form.

    Attributes
    ----------
    _init_fmt : str
        The format for the initial statement.
    _main_fmt : str
        The format for the fields.
    _main_fmt_len : int
        The length of the _main_fmt devoid of color.
    _msg_fmt : str
        The format for the current active field's message.
    _default_fmt : str
        The format for fields' default message (if there is one).
    _num_fields : int
        The number of fields.
    """

    __name__ = 'Form'
    __module__ = 'cues'

    def __init__(self, name: str, message: str, fields: Iterable[dict]):
        """

        Parameters
        ----------
        name
            The name of the Form instance.
        message
            Instructions or useful information regarding the prompt for the user.
        fields
            Contains questions/information for the user to respond to.
        """

        super().__init__(name, message)

        if hasattr(fields, '__iter__'):
            self._fields = list(fields)
        else:
            raise TypeError(f"'{type(fields)}' object is not iterable")

        self._init_fmt = '[pink][?][/pink] {message}\n'
        self._main_fmt = '[skyblue]{marker}[/skyblue]  {:>{len}} [grey]∙[/grey] {text}\n'
        self._main_fmt_len = 6
        self._msg_fmt = '[lightslateblue]{}[/lightslateblue]'
        self._default_fmt = '[darkgrey]{}[/darkgrey]'

        self._num_fields = len(self._fields)

    def send(self):
        """Returns a dict object containing user's response to the prompt.

        Returns
        -------
        dict
            Contains the user's response to the prompt.
        """

        self._draw()
        return self.answer

    def _draw(self):
        """Assembles and prints the form prompt to the console.
        """

        cursor.write(self._init_fmt.format(message=self._message), color=True)

        up = self.keys.get('up')
        down = self.keys.get('down')
        left = self.keys.get('left')
        right = self.keys.get('right')
        enter = self.keys.get('enter')
        backspace = self.keys.get('backspace')

        inputs = ['' for _ in range(self._num_fields)]
        max_msg_len = max(len(field.get('message')) for field in self._fields)
        # The total space taken up by self._main_fmt:
        padding = max_msg_len + self._main_fmt_len

        defaults = [
            self._default_fmt.format(field.get('default', '')) for field in self._fields]

        curr_row = 0
        x_cursor_pos = 0
        y_cursor_pos = 0
        self.__num = self._num_fields

        while True:
            self.__set_num_rows(inputs, padding)
            # self.update_cursor_position()
            self.__print_fields(inputs, defaults, curr_row, max_msg_len)
            # self.__set_num_rows(inputs, padding)

            curr_input_len = len(inputs[curr_row])
            prev_curr_input_len = curr_input_len

            # div = self.__num_rows[curr_row] - 1
            div, mod = divmod(padding + curr_input_len, self.max_columns)

            # total_rows = sum(self.__num_rows)
            total_rows = self._num_fields
            x_displacement = (mod or self.max_columns) - x_cursor_pos
            # x_displacement = curr_input_len - x_cursor_pos
            y_displacement = y_cursor_pos - sum(self.__num_rows[curr_row + 1:])
            if x_displacement < 0:
                temp_div, temp_mod = divmod(
                    abs(x_displacement), self.max_columns)
                if temp_mod:
                    temp_div += 1
                # temp_div += 1
                # if not temp_mod:
                #     temp_div -= 1
                x_displacement = divmod(
                    padding + curr_input_len - mod - abs(x_displacement), self.max_columns)[1]
                y_displacement -= temp_div

                # add_y, x_displacement = divmod(
                #     padding + curr_input_len - mod - abs(x_displacement), self.max_columns)
                # y_displacement -= (add_y or 1)
                #
                #
                # temp_curr_input_len = padding + curr_input_len - mod
                # y_displacement -= 1
                # x_displacement = temp_curr_input_len - abs(x_displacement)
            cursor.move(x=x_displacement,
                        y=total_rows - y_displacement)
            # cursor.move(x=(mod if div and mod else padding + x_displacement),
            #             y=total_rows - y_displacement)

            key = self.listen_for_key()

            if key == up:
                if y_cursor_pos:
                    y_cursor_pos -= 1
                    curr_row -= 1
                    curr_input_len, prev_curr_input_len, x_cursor_pos = self.__reset_values(
                        curr_input_len, prev_curr_input_len, x_cursor_pos)

            elif key == down:
                if y_cursor_pos != (total_rows - 1):
                    y_cursor_pos += 1
                    curr_row += 1
                    curr_input_len, prev_curr_input_len, x_cursor_pos = self.__reset_values(
                        curr_input_len, prev_curr_input_len, x_cursor_pos)

            elif key == left:
                if x_cursor_pos != curr_input_len:
                    x_cursor_pos += 1

            elif key == right:
                if x_cursor_pos:
                    x_cursor_pos -= 1

            elif key == backspace:
                if curr_input_len - x_cursor_pos:
                    inputs[curr_row] = utils.delete(
                        inputs[curr_row], curr_input_len - x_cursor_pos)
                    prev_curr_input_len = 0

            elif key == enter:
                if y_cursor_pos == (total_rows - 1):
                    cursor.move(x=-self.max_columns,
                                y=-total_rows + y_displacement)
                    cursor.clear(self._num_fields + sum(self.__num_rows))
                    break

                y_cursor_pos += 1
                curr_row += 1
                curr_input_len, prev_curr_input_len, x_cursor_pos = self.__reset_values(
                    curr_input_len, prev_curr_input_len, x_cursor_pos)

            else:
                inputs[curr_row] = utils.insert(
                    chr(key), inputs[curr_row], len(inputs[curr_row]) - x_cursor_pos)
                # if x_displacement < 0 and not mod:
                #     y_displacement -= 1
                #
                #
                # inputs[curr_row] = utils.insert(
                #     chr(key), inputs[curr_row], x_displacement)

            # Drops cursor below all main_fmt:
            cursor.move(x=-self.max_columns,
                        y=-total_rows + y_displacement)

            y_delta = self._num_fields + sum(self.__num_rows)
            #
            # prev_y_pos = self.y
            # self.update_cursor_position()
            # y_delta = self.y - prev_y_pos

            if not prev_curr_input_len and len(inputs[curr_row]):
                # Refreshes output to remove traces of default messages:
                cursor.clear(y_delta)
                # cursor.clear(total_rows +
                #              sum(self.__num_rows[curr_row + 1:]) + div)
            elif div and not mod:
                cursor.clear(y_delta)
                # cursor.clear(total_rows + (div - 1) +
                #              sum(self.__num_rows[:curr_row + 1]))
            else:
                # Puts cursor just below init_fmt:
                cursor.move(y=y_delta)
                # cursor.move(y=total_rows +
                #             sum(self.__num_rows[:curr_row + 1]))
                #
                #
                # cursor.move(y=total_rows + (div if mod else div - 1))

        answer = {self._name: {}}
        for i, f in zip(inputs, self._fields):
            answer.get(self._name).update(
                {f['message']: i or f.get('default', '')})
        self.answer = answer

        #
        #
        #
        #

    def __print_fields(self, inputs: list, defaults: list, curr_row: int,
                       max_msg_len: int):
        """Prints the fields to the console.

        Parameters
        ----------
        inputs
            Current responses from the user.
        defaults
            The default strings for each field.
        curr_row
            The current field that is currently in focus.
        max_msg_len
            The message among the fields with the largest length.
        """

        for c, field, in enumerate(self._fields):
            # If we're on the current row, then give the message color:
            msg = field.get('message')
            if curr_row == c:
                # Get the length before the message is colored:
                msg_len = len(msg)
                msg = self._msg_fmt.format(field.get('message'))
                # Then get the lenght after the message is colored:
                color_msg_len = len(msg)
                color_msg_diff = color_msg_len - msg_len
            else:
                color_msg_diff = 0

            # If the current input has content, then give it a filled marker
            # otherwise, give it an empty marker:
            marker = constants.FORM_MARKER_COM if inputs[c] else constants.FORM_MARKER_UNC
            # For each input that's empty, replace it with one of the defaults:
            text = inputs[c] or defaults[c]

            cursor.write(self._main_fmt.format(
                msg, marker=marker, len=max_msg_len + color_msg_diff, text=text), color=True)

    def __set_num_rows(self, inputs: list, padding: int):
        """Sets the number of additional rows based on inputs.

        This private method will calculate the number of additional rows that each
        current field's input takes up. It uses the maximum number of columns available
        to calculate excess rows.

        Note
        ----
        An excess row is only counted if there is a remainder. In other words, if there
        are is an input that amounts to 120 while the maximum number of columns is also
        120, the number of excess rows will still be 0 since ``120 % 120 == 0``.

        Parameters
        ----------
        inputs
            Current responses from the user.
        padding
            The total number of columns taken up by the message among the fields with the
            largest length and ``self._main_fmt``.
        """

        num_rows = []
        for i in inputs:
            div, mod = divmod(len(i) + padding, self.max_columns)
            num_rows.append(div if mod else div - 1)
        self.__num_rows = num_rows
        #
        # self.__num_rows = [
        #     divmod(len(i) + padding, self.max_columns)[0] for i in inputs]
        #
        # self.__num_rows = [self.__num]

    def __reset_values(self, *args):
        return (0 for _ in range(len(args)))

    @classmethod
    def from_dict(cls, prompt: dict):
        """Creates and instantiates a Form object from a dict object.

        Parameters
        ----------
        prompt
            A dict that contains a name key, a message key, and a
            fields key.

        Returns
        -------
        cues.Form
            A Form object to retrieve a single response from a user.
        """

        name = prompt['name']
        message = prompt['message']
        fields = prompt['fields']
        return cls(name, message, fields)


def main(test=0):
    name = 'basic_info'
    message = 'Please fill out the following form:'
    fields = [
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
            'message': 'What is your favorite programming language?'
        }
    ]

    if not test:
        prompt = Form(name, message, fields)
        answer = prompt.send()
        print(answer)


if __name__ == '__main__':
    main()
