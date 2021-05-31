# -*- coding: utf-8 -*-

"""
cues.cue
========

This module contains the class for creating and instantiating `Cue` objects.
"""

import subprocess
from abc import abstractmethod
from collections import deque
from typing import Deque

from . import utils
from .canvas import Canvas


class Cue(Canvas):
    """The abstract base class for all child Cue objects.

    Note
    ----
    This class contains abstractmethods which means you should not instantiate
    it.

    Attributes
    ----------
    _name : str
        The name of the Cue instance.
    _message : str
        Instructions or useful information regarding the prompt for the user.
    keys : dict
        Blend of different keypresses.
    listen_for_key : FunctionType
        Function that listens for keypresses based on OS.
    _answer : dict
        The answer to return once the user successfully responds to a Cue object.
    """

    __name__ = 'Cue'
    __module__ = 'cues'

    def __init__(self, name: str, message: str):
        """

        Parameters
        ----------
        name
            The name of the Cue instance.
        message
            Instructions or useful information regarding the prompt for the user.
        """

        super().__init__()

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

        # Gathers all possible key presses into a dict:
        self.keys = utils.get_keys()
        # Chooses which key listening function to use based on OS:
        self.listen_for_key = utils.get_listen_function()

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
    def create_deque(lis: list, length: int = None) -> Deque[str]:
        """Returns a deque object containing strings.

        Parameters
        ----------
        lis
            A list of objects that can be converted to str objects.
        length : int, optional
            A value that can be used to set the maxlen parameter of the deque()
            function.

        Returns
        -------
        Deque of str
            A list converted into a deque with a set maxlen.
        """

        container = []
        for elem in lis:
            container.append(str(elem))

        d = deque(container, maxlen=(length or len(container)))
        return d
