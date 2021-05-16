"""
cues.cues
=========

A module that contains the class for creating and instantiating `Cue` objects.
"""

import copy
import shutil
import subprocess
import sys
from abc import ABC, abstractmethod
from collections import deque
from typing import Deque, Iterable, List

from . import color, constants, cursor, listen, utils
from .listen import ansi, unix, windows


class Cue(ABC):
    """The abstract base class for all child Cue objects.

    This class contains abstract methods so you cannot instantiate this object.

    Parameters
    ----------
    name : str
        A str object to retrieve the user's input once formatted in a dict
        object.
    message : str
        A str object that displays useful information for the user to the
        console.
    """

    __name__ = 'Cue'
    __module__ = 'cues'

    def __init__(self, name: str, message: str):
        """Inits a Cue child class with `name` and `message`.

        Attributes
        ----------
        _answer : None
            Defaults to None.
            Can be interacted with as a property attribute (getter, setter)
            and is intended to be returned as a dict object.
        """

        # Enables color in the console for Windows machines:
        if utils.is_windows():
            subprocess.call('color', shell=True)

        if isinstance(name, str):
            self._name = name
        else:
            raise TypeError(f"'{type(name)}' object is not a str object")

        if isinstance(message, str):
            self._message = message
        else:
            raise TypeError(f"'{type(message)}' object is not a str object")

        self._answer = None

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, answer: dict):
        self._answer = answer

    @abstractmethod
    def send(self):
        pass

    @abstractmethod
    def _draw(self):
        pass

    @staticmethod
    def create_deque(lis: list, length=None) -> Deque[str]:
        """Returns a deque object.

        Parameters
        ----------
        lis : list
            A list of objects that can be converted to str objects.
        length : int, optional
            A value that can be used to set the maxlen parameter of the deque()
            function.

        Returns
        -------
        d : deque
            A list converted into a deque with a set maxlen.
        """

        container = []
        for elem in lis:
            container.append(str(elem))

        d = deque(container, maxlen=(length or len(container)))
        return d


class Select(Cue):
    """Construct a Select object to retrieve a single response from a user.

    A Select object will display a menu-like prompt to the user
    and ask the user to select one option. The user can use the
    Up and Down arrow keys to navigate the prompt and select an
    option by pressing Enter.

    Parameters
    ----------
    name : str
        A str object to retrieve the user's input once formatted in a dict
        object.
    message : str
        A str object that displays useful information for the user to the
        console.
    options : iterable of str
        An iterable of str objects to be used as menu options for the user
        to choose from.
    """

    __name__ = 'Select'
    __module__ = 'cues'

    def __init__(self, name: str, message: str, options: Iterable[str]):
        """Inits a Select class with `name`, `message`, and `option`.

        Attributes
        ----------
        _num_options : int
            The number of options
        _markers : Deque of str
            A deque of str objects that contains an arrow marker and empty
            spaces to indicate to the user which option is currently
            selected.
        _select_marker_len : int
            The length of the arrow marker being used.
        _init_fmt : str
            A str object with the format for the initial statement.
        _list_fmt : str
            A str object with the format for list items.
        _list_fmt_if_active : str
            A str object with the format for active list items.
        """
        super().__init__(name, message)

        if hasattr(options, '__iter__'):
            self._options = list(options)
            self._num_options = len(self._options)
        else:
            raise TypeError(f"'{type(options)}' object is not iterable")

        # Create the deque that will contain the arrow markers and
        # allocate an appropriate number of arrow marker spaces depending
        # on the number of options:
        self._markers = self.create_deque(
            [constants.SELECT_MARKER], length=self._num_options)

        self._select_marker_len = len(constants.SELECT_MARKER)

        for _ in range(self._num_options - 1):
            self._markers.append(' ' * self._select_marker_len)

        self._init_fmt = '[pink][?][/pink] {message}\n'
        self._list_fmt = '[skyblue]{marker}[/skyblue] {option}'
        self._list_fmt_if_active = '[skyblue]{marker}[/skyblue] [underline skyblue]{option}[/underline skyblue]'

    @property
    def options(self) -> List[str]:
        return self._options

    @property
    def markers(self) -> Deque[str]:
        return self._markers

    @markers.setter
    def markers(self, pos: int):
        # If the keystroke was the up arrow:
        if pos:
            # If the LIST_MARKER is the first element in the deque:
            if not self._markers.index(constants.LIST_MARKER):
                self._markers.append(constants.LIST_MARKER)
            else:
                self._markers.append(' ' * self._select_marker_len)

        # Otherwise, if the keystroke was the down arrow:
        else:
            # If the LIST_MARKER is the last element in the deque:
            if self._markers.index(constants.LIST_MARKER) == self._num_options - 1:
                self._markers.appendleft(constants.LIST_MARKER)
            else:
                self._markers.appendleft(' ' * self._select_marker_len)

    def send(self) -> dict:
        """Returns a dict object containing user's response to the prompt.

        Returns
        -------
        self.answer : dict
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

        # The initial statement to print (which contains the user's message):
        # init_statement = '[pink][?][/pink] ' + self._message + '\n'
        cursor.write(self._init_fmt.format(message=self._message), color=True)

        # Different formats based on which option is currently highlighted:
        # list_fmt = '[skyblue]{marker}[/skyblue] {option}'
        # list_fmt_if_arrow = '[skyblue]{marker}[/skyblue] [underline skyblue]{option}[/underline skyblue]'

        # Chooses which key listening function to use based on OS:
        listen_for_key = utils.get_listen_function()

        keys = utils.get_keys()
        up = keys.get('up')
        down = keys.get('down')
        enter = keys.get('enter')

        while True:
            for marker, option in zip(self.markers, self.options):
                fmt = (self._list_fmt if marker !=
                       constants.LIST_MARKER else self._list_fmt_if_active) + '\n'

                cursor.write(fmt.format(
                    marker=marker, option=option), color=True)

            key = listen_for_key()

            if key == up:
                self.markers = 1
            elif key == down:
                self.markers = 0
            elif key == enter:
                break

            # Clears num of lines above the current cursor position:
            cursor.clear(self._num_options)

        # Sets answer:
        list_marker_pos = self._markers.index(constants.LIST_MARKER)
        self.answer = {self._name: self.options[list_marker_pos]}

    @classmethod
    def from_dict(cls, prompt: dict):
        """Creates and instantiates a Select object from a dict object.

        Parameters
        ----------
        prompt : dict
            A dict object that contains a name key, a message key, and an
            options key.

        Returns
        -------
        cues.Select
            A Select object to retrieve a single response from a user.
        """

        name = prompt['name']
        message = prompt['message']
        options = prompt['options']
        return cls(name, message, options)


class Confirm(Cue):
    """Construct a Confirm object to retrieve a True or False response from a user.

    A Confirm object will display a yes-or-no prompt to the user
    and ask the user to answer yes or no. The user must use the y
    key or the n key to respond.

    Parameters
    ----------
    name : str
        A str object to retrieve the user's input once formatted in a dict
        object.
    message : str
        A str object that displays useful information for the user to the
        console.
    _confirm_fmt : str
        A str object that contains the format for the confirm prompt.
    """

    __name__ = 'Confirm'
    __module__ = 'cues'

    def __init__(self, name: str, message: str):
        """Inits a Confirm class with `name` and `message`.
        """

        super().__init__(name, message)

        self._confirm_fmt = '{prompt} [grey]∙[/grey] [darkgrey]{confirm}[/darkgrey]  {r}{end}'

    def send(self) -> dict:
        """Returns a dict object containing user's response to the prompt.

        Returns
        -------
        self.answer : dict
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

        confirm = '(y/N)'
        end = '\r'

        # Chooses which key listening function to use based on OS:
        listen_for_key = utils.get_listen_function()

        keys = utils.get_keys()
        y = keys.get('y')
        Y = keys.get('Y')
        n = keys.get('n')
        N = keys.get('N')

        cursor.write(self._confirm_fmt.format(
            prompt=self._message, confirm=confirm, r='', end=end), color=True)

        while True:
            key = listen_for_key()

            if key == y or key == Y:
                answer = True
                break
            elif key == n or key == N:
                answer = False
                break

        end = '\n'
        cursor.write(self._confirm_fmt.format(prompt=self._message, confirm=confirm, r=(
            'Yes' if answer else 'No'), end=end), color=True)

        self.answer = {self._name: answer}

    @classmethod
    def from_dict(cls, prompt: dict):
        """Creates and instantiates a Confirm object from a dict object.

        Parameters
        ----------
        prompt : dict
            A dict object that contains a name key, a message key, and an
            options key.

        Returns
        -------
        cues.Confirm
            A Confirm object to retrieve a single response from a user.
        """

        name = prompt['name']
        message = prompt['message']
        return cls(name, message)


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
    __module__ = 'cues'

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
            A str object with the format for the default messages.
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
            A dict object that contains a name key, a message key, and an
            options key.

        Returns
        -------
        cues.Form
            A Form object to retrieve a single response from a user.
        """

        name = prompt['name']
        message = prompt['message']
        fields = prompt['fields']
        return cls(name, message, fields)


class Survey(Cue):
    """Construct a Survey object to retrieve one or more responses from a user.

    A Survey object will display a sequence of questions to the user
    and ask the user to answer them by using a scale. The user can
    use the Right and Left arrow keys to select an option on the scale
    and press Enter to move to the next question.

    Parameters
    ----------
    name : str
        A str object to retrieve the user's input once formatted in a dict
        object.
    message : str
        A str object that displays useful information for the user to the
        console.
    scale : iterable
        An iterable of objects (mainly str or int) to be used as the range
        of the scale.
    fields : iterable of dict
        An iterable of dict objects that contain information about the survey
        questions.
    legend : iterable
        An iterable of objects (mainly str) to be used to define the values
        of the scale.
    """

    __name__ = 'Survey'
    __module__ = 'cues'

    def __init__(self, name: str, message: str, scale: Iterable,
                 fields: Iterable[dict], legend: Iterable = []):
        """Inits a Form class with `name`, `message`, `scale`, and `fields`.

        Attributes
        ----------
        _scale : list of objects
            A list of objects to use as the range for the scale.
        _fields : list of dict
            A list object containing dicts (fields) to construct a survey.
        _legend : list of str
            A list object containing str objects that defines values for
            _scale.
        _legend_fmt : str
            A str object with the format for the legend.
        _header_fmt : str
            A str object with the format for the legend header.
        _space_btwn : int
            A constant integer representing the space between legend values.
            This is only used if there are only two legend values.
        _total_legend_fmt_len : int
            An integer representing the total space between the header.
            This is only used if there are only two legend values.
        _init_fmt : str
            A str object with the format for the initial statement.
        _msg_fmt : str
            A str object with the format for the message.
        _pt_fmt : str
            A str object with the format for the number of points in the scale.
        _scale_fmt : str
            A str object with the format for the values of the scale.
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
        self.answer : dict
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

        # Chooses which key listening function to use based on OS:
        listen_for_key = utils.get_listen_function()

        keys = utils.get_keys()
        right = keys.get('right')
        left = keys.get('left')
        enter = keys.get('enter')

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

            key = listen_for_key()

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
            A dict object that contains a name key, a message key, and an
            options key.

        Returns
        -------
        cues.Survey
            A Survey object to retrieve a single response from a user.
        """

        name = prompt['name']
        message = prompt['message']
        scale = prompt['scale']
        fields = prompt['fields']
        return cls(name, message, scale, fields)
