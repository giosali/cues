"""
cues.form
=========

A module that contains the Form class.
"""

import shutil
from typing import Deque, Iterable, List

from . import constants, cursor, utils
from .cue import Cue


class Form(Cue):
    """Construct a Form object to retrieve several responses from a user.

    A Form object will display a form-like prompt to the user
    and ask the user to answer corresponding questions. The user 
    can type their answers and use Up and Down arrow keys and the 
    Enter key to navigate the form.

    Parameters
    ----------
    name : str
        A str object to retrieve the user's input once formatted in a dict
        object.
    message : str
        A str object that displays useful information for the user to the
        console.
    fields : iterable of dict
        An iterable of dict objects that contain information about the form
        questions.
    _init_fmt : str
        A str object with the format for the initial statement.
    _main_fmt : str
        A str object with the format for the fields.
    _msg_fmt : str
        A str object with the format for messages in active fields.
    _default_fmt : str
        A str object with the fomrat for default messages.
    """

    __name__ = 'Form'
    __module__ = 'form'

    def __init__(self, name: str, message: str, fields: Iterable[dict]):
        """Inits a Form class with `name`, `message`, and `fields`.

        Attributes
        ----------
        _fields : list of dict
            A list object containing dicts (fields) to construct a form.
        _init_fmt : str
            A str object with the format for the initial statement.
        _main_fmt : str
            A str object with the format for the frame of the form.
        _msg_fmt : str
            A str object with the format for the form's messages. This is
            also used to highlight messages.
        _default_fmt : str
            A str object with the format for default messages.
        """

        super().__init__(name, message)

        if hasattr(fields, '__iter__'):
            self._fields = list(fields)
        else:
            raise TypeError(f"'{type(fields)}' object is not iterable")

        self._init_fmt = '[pink][?][/pink] {message}\n'
        self._main_fmt = '[skyblue]{marker}[/skyblue]  {:>{len}} [grey]∙[/grey] {text}\n'
        self._msg_fmt = '[lightslateblue]{}[/lightslateblue]'
        self._default_fmt = '[darkgrey]{}[/darkgrey]'

    def send(self):
        """Returns a dict object containing user's response to the prompt.

        Returns
        -------
        self.answer : dict
            A dict containing the user's response to the prompt.
        """

        self._draw()
        return self.answer

    def _draw(self):
        """Prints the prompt to console and sets user's response.
        """

        cursor.write(self._init_fmt.format(message=self._message), color=True)

        # Determines how much space to give for the fields' messages:
        max_msg_len = max(len(msg['message']) for msg in self._fields)
        # min_col will be used for the horizontal starting point
        # The six comes from manually counting the spaces in
        # self._main_fmt. There's probably a better way of doing this.
        min_col = max_msg_len + 6

        # Chooses which key listening function to use based on OS:
        listen_for_key = utils.get_listen_function()

        keys = utils.get_keys()
        up = keys.get('up')
        down = keys.get('down')
        enter = keys.get('enter')
        backspace = keys.get('backspace')

        # Starting position for the cursor, in terms of the number of rows **from
        # the bottom**, should be equal to the number of fields in the form, assuming
        # each field only takes a line of space:
        num_fields = len(self._fields)
        row_num = num_fields
        prev_row_num = row_num

        max_num_cols = shutil.get_terminal_size().columns

        # Records the characters entered by user:
        usr_inputs = ['' for _ in range(num_fields)]

        # Color the default messages:
        defaults = [
            self._default_fmt.format(field.get('default', '')) for field in self._fields]

        curr_row_pos = num_fields - row_num
        row_spans = [0 for _ in range(num_fields)]
        superficial_row_num = 0

        while True:
            # Prints the fields to the console:
            for c, field in enumerate(self._fields):
                msg = field['message']
                msg_diff = 0
                if c == curr_row_pos:
                    init_msg_len = len(msg)
                    msg = self._msg_fmt.format(msg)
                    msg_diff = len(msg) - init_msg_len

                marker = constants.FORM_MARKER_COM if usr_inputs[c] else constants.FORM_MARKER_UNC
                text = usr_inputs[c] or defaults[c]

                cursor.write(self._main_fmt.format(
                    msg, marker=marker, len=max_msg_len + msg_diff, text=text), color=True)

            # Sets where the cursor should be:
            curr_input_len = len(usr_inputs[curr_row_pos]) + min_col
            curr_input_row_span = 0
            while curr_input_len > max_num_cols:
                curr_input_row_span += 1
                curr_input_len -= max_num_cols
            row_spans[curr_row_pos] = curr_input_row_span

            cursor.move(curr_input_len, row_num + superficial_row_num)

            # Used to access `usr_inputs`:
            curr_row_pos = num_fields - row_num
            prev_curr_row_pos = curr_row_pos
            superficial_row_num = 0

            key = listen_for_key()

            if key == up:
                # If cursor pos is at the very top:
                if row_num == num_fields:
                    pass
                else:
                    row_num += 1
                    curr_row_pos = num_fields - row_num
            elif key == down:
                # If cursor pos is at the very bottom:
                if row_num == 1:
                    pass
                else:
                    row_num -= 1
                    curr_row_pos = num_fields - row_num
            elif key == backspace:
                # Get the input at the current line/row:
                curr_input = usr_inputs[curr_row_pos]
                # Replace it with curr_input but remove one char at the end:
                usr_inputs[curr_row_pos] = curr_input[:len(curr_input) - 1]
            elif key == enter:
                # If `enter` is pressed on last row, quit
                if row_num == 1:
                    sum_row_spans = sum(
                        i for c, i in enumerate(row_spans) if c > prev_curr_row_pos)
                    cursor.move(-max_num_cols, -prev_row_num - sum_row_spans)
                    cursor.clear(num_fields + sum(row_spans))
                    break
                # Else move cursor down a row:
                row_num -= 1
                curr_row_pos = num_fields - row_num
            else:
                usr_inputs[curr_row_pos] += chr(key)

            # Gets proper number of rows to adjust Y coordinate:
            for c, i in enumerate(row_spans):
                if c > curr_row_pos:
                    superficial_row_num += row_spans[c]

            # Drops cursor at the bottom:
            sum_row_spans = sum(
                i for c, i in enumerate(row_spans) if c > prev_curr_row_pos)
            cursor.move(-max_num_cols, -prev_row_num - sum_row_spans)

            prev_row_num = row_num

            # In case text overflow occurs:
            cursor.clear(num_fields + sum(row_spans))

        for c, i in enumerate(usr_inputs):
            if not i:
                usr_inputs[c] = self._fields[c].get('default', '')

        field_names = [field['name'] for field in self._fields]
        self.answer = {self._name: {name: i for name,
                                    i in zip(field_names, usr_inputs)}}

    @classmethod
    def from_dict(cls, prompt: dict):
        """Creates and instantiates a Form object from a dict object.

        Parameters
        ----------
        prompt : dict
            A dict object that contains a name key, a message key, and a
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
