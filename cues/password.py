# -*- coding: utf-8 -*-

"""
cues.password
=============

This module contains the Password class.
"""

from . import cursor
from .cue import Cue
from .listen import ansi


class Password(Cue):
    """Construct a Password object to retrieve hidden input from the user.

    Password objects are useful when you require input from the user but
    would like their input to be hidden as they type as it may contain
    sensitive information.

    Attributes
    ----------
    _password_fmt : str
        The format for the password prompt.
    """

    __name__ = 'password'
    __module__ = 'cues'

    def __init__(self, name: str, message: str):
        """

        Parameters
        ----------
        name
            The name of the Form instance.
        message
            Instructions or useful information regarding the prompt for the user.
        """

        super().__init__(name, message)

        if message.strip()[-1].isalnum():
            self._password_fmt = '[pink][?][/pink] {message} [grey]∙[/grey] {input}'
            self._password_fmt_len = 7
        else:
            self._password_fmt = '[pink][?][/pink] {message} {input}'
            self._password_fmt_len = 5

    def send(self) -> dict:
        """Returns a dict object containing user's response to the prompt.

        Returns
        -------
        dict
            Contains the user's response to the prompt.
        """

        self._draw()
        return self.answer

    def _draw(self):
        """Assembles and prints the Password cue to the console.
        """

        up = self.keys.get('up')
        down = self.keys.get('down')
        right = self.keys.get('right')
        left = self.keys.get('left')
        backspace = self.keys.get('backspace')
        enter = self.keys.get('enter')

        padding = self._password_fmt_len + len(self._message)
        input = ''
        password = ''
        buffer = ''

        while True:
            cursor.write(buffer + self._password_fmt.format(
                message=self._message, input=password), color=True)

            div, mod = divmod(padding + len(input), self.max_columns)
            if not mod:
                div -= 1

            buffer = ''
            for _ in range(div + 1):
                buffer = ((ansi.CLEAR_ENTIRE_LINE + ansi.UP_ONE) * div) + \
                    ansi.CLEAR_ENTIRE_LINE

            key = self.listen_for_key()

            if key == backspace:
                input = input[:-1]
                password = password[:-1]

            elif key == enter:
                cursor.move(x=-self.max_columns)
                cursor.write(buffer)
                break

            elif (key == up) or (key == down) or (key == right) or (key == left):
                pass

            else:
                input += chr(key)
                password += '*'

            cursor.move(x=-self.max_columns)

        self.answer = {self._name: input}

    @classmethod
    def from_dict(cls, prompt: dict):
        """Creates and instantiates a Password object from a dict object.

        Parameters
        ----------
        prompt
            A dict that contains a name key and a message key.

        Returns
        -------
        cues.Password
            A Password object to retrieve a single response from a user.
        """

        name = prompt['name']
        message = prompt['message']
        return cls(name, message)


def main():
    name = 'password'
    message = 'Password:'

    prompt = Password(name, message)
    answer = prompt.send()
    print(answer)


if __name__ == '__main__':
    main()
