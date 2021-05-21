"""
cues.checkbox
=============

A module that contains the Checkbox class.
"""

from typing import Iterable

from . import constants, cursor, utils
from .cue import Cue


class Checkbox(Cue):
    """Construct a Checkbox object to retrieve none, one, or more responses from a user.

    A Checkbox object will display a series of options to the user
    and ask the user to choose as many as they would like. The user can
    use the Up and Down arrow keys to maneuver through options, use
    the Space key to choose options, and press Enter to submit their choices.

    Parameters
    ----------
    name : str
        A str object to retrieve the user's input once formatted in a dict
        object.
    message : str
        A str object that displays useful information for the user to the
        console.
    options : iterable of str
        An iterable of strings to be used as the available options for the
        user to pick from.
    """

    __name__ = 'Checkbox'
    __module__ = 'cues'

    def __init__(self, name: str, message: str, options: Iterable[str]):
        """Inits a Form class with `name`, `message`, `scale`, and `fields`.

        Attributes
        ----------
        _options : iterable of str
            A list of str objects to use as the available options for the user
            to pick from.
        _init_fmt : str
            A str object with the format for the initial statement.
        _list_fmt : str
            A str object with the format for elements in _options.
        _list_fmt_if_active : str
            A str object with a specific list format to use if the current element
            in _options is currently in focus.
        """

        super().__init__(name, message)

        if hasattr(options, '__iter__'):
            self._options = list(options)
        else:
            raise TypeError(f"'{type(options)}' object is not iterable")

        self._init_fmt = '[pink][?][/pink] {message}'
        self._list_fmt = '[darkgrey]{marker}[/darkgrey] {option}'
        self._list_fmt_if_active = '[lightslateblue]{marker}[/lightslateblue] [underline skyblue]{option}[/underline skyblue]'

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

        cursor.write(self._init_fmt.format(
            message=self._message), color=True, newlines=1)

        # Chooses which key listening function to use based on OS:
        listen_for_key = utils.get_listen_function()

        keys = utils.get_keys()
        up = keys.get('up')
        down = keys.get('down')
        space = keys.get('space')
        enter = keys.get('enter')

        # Get appropriate num of markers based on num of options:
        num_options = len(self._options)
        markers = [constants.FORM_MARKER_UNC for _ in range(num_options)]

        colored_form_marker_com = '[lightslateblue]' + \
            constants.FORM_MARKER_COM + '[/lightslateblue]'
        curr_row = num_options
        while True:
            curr_row_diff = num_options - curr_row
            for c, (marker, option) in enumerate(zip(markers, self._options)):
                fmt = self._list_fmt_if_active if c == curr_row_diff else self._list_fmt

                cursor.write(fmt.format(
                    marker=marker, option=option), color=True, newlines=1)

            key = listen_for_key()

            if key == up:
                if not curr_row_diff:
                    curr_row = 1
                    # pass
                else:
                    curr_row += 1

            elif key == down:
                if curr_row_diff == num_options - 1:
                    curr_row = num_options
                    # pass
                else:
                    curr_row -= 1

            elif key == space:
                if markers[curr_row_diff] == constants.FORM_MARKER_UNC:
                    markers[curr_row_diff] = colored_form_marker_com
                else:
                    markers[curr_row_diff] = constants.FORM_MARKER_UNC

            elif key == enter:
                cursor.clear(num_options)
                break

            # Moves cursor to the top:
            cursor.move(y=num_options)

        selected_options = []
        for c, marker in enumerate(markers):
            if marker == colored_form_marker_com:
                selected_options.append(self._options[c])
        self.answer = {self._name: selected_options}

    @classmethod
    def from_dict(cls, prompt: dict):
        """Creates and instantiates a Checkbox object from a dict object.

        Parameters
        ----------
        prompt : dict
            A dict object that contains a name key, a message key, and an
            options key.

        Returns
        -------
        cues.Checkbox
            A Checkboc object to retrieve none, one, or more responses from a user.
        """

        name = prompt['name']
        message = prompt['message']
        options = prompt['options']
        return cls(name, message, options)


def main(test=0):
    name = 'guitars'
    message = 'Pick your favorite guitars:'
    options = [
        'Les Paul',
        'Stratocaster',
        'Telecaster',
        'SG',
        'Flying V',
        'Acoustic',
        'Classical',
    ]

    if not test:
        cue = Checkbox(name, message, options)
        answer = cue.send()
        print(answer)


if __name__ == '__main__':
    main()
