"""
cues.confirm
==============

A module that contains the Confirm class.
"""

from . import cursor, utils
from .cue import Cue


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
    __module__ = 'confirm'

    def __init__(self, name: str, message: str):
        """Inits a Confirm class with `name` and `message`.
        """

        super().__init__(name, message)

        self._confirm_fmt = '[pink][?][/pink] {prompt} [grey]∙[/grey] [darkgrey]{confirm}[/darkgrey]  {r}{end}'

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
            A dict object that contains a name key and a message key.

        Returns
        -------
        cues.Confirm
            A Confirm object to retrieve a single response from a user.
        """

        name = prompt['name']
        message = prompt['message']
        return cls(name, message)


def main(test=0):
    name = 'continue'
    message = 'Are you sure you want to continue?'

    if not test:
        prompt = Confirm(name, message)
        answer = prompt.send()
        print(answer)


if __name__ == '__main__':
    main()
