# -*- coding: utf-8 -*-

"""
cues.checkbox
=============

This module contains the Checkbox class.
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

    Attributes
    ----------
     _options : list of str
        The available options for the user to pick from.
    _init_fmt : str
        The format for the initial statement.
    _list_fmt : str
        The format for ``_options``.
    _list_fmt_if_active : str
        The format for the current active element in ``_options``.
    """

    __name__ = 'Checkbox'
    __module__ = 'cues'

    def __init__(self, name: str, message: str, options: Iterable[str]):
        """

        Parameters
        ----------
        name
            The name of the Checkbox instance.
        message
            Instructions or useful information regarding the prompt for the user.
        fields
            Available options for the user to pick from.
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

        up = self.keys.get('up')
        down = self.keys.get('down')
        space = self.keys.get('space')
        enter = self.keys.get('enter')

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

            key = self.listen_for_key()

            if key == up:
                if not curr_row_diff:
                    curr_row = 1
                else:
                    curr_row += 1

            elif key == down:
                if curr_row_diff == num_options - 1:
                    curr_row = num_options
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
        prompt
            A dict that contains a name key, a message key, and an
            options key.

        Returns
        -------
        cues.Checkbox
            A Checkbox object to retrieve none, one, or more responses from a user.
        """

        name = prompt['name']
        message = prompt['message']
        options = prompt['options']
        return cls(name, message, options)


def main():
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

    cue = Checkbox(name, message, options)
    answer = cue.send()
    print(answer)


if __name__ == '__main__':  # pragma: no cover
    main()
