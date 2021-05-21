"""
cues.cue
=========

A module that contains the class for creating and instantiating `Cue` objects.
"""

import subprocess
from abc import ABC, abstractmethod
from collections import deque
from typing import Deque

from . import utils


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
    __module__ = 'cue'

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
