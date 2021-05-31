# -*- coding: utf-8 -*-

"""
cues.canvas
===========

This module contains the Canvas class for interpreting and reading information about the console and current output.
"""

import shutil
import traceback
from abc import ABC

from . import utils


class Canvas(ABC):
    """Abstract base class for handling the console and current output.

    Note
    ----
    The starting position of the console screen at any point is at 
    (0, 0) (top-left corner of the console). Moving to the right adds
    to the x-coordinate. Moving to the left subtracts from the x-coordinate.
    Moving down adds to the y-coordinate. Moving up subtracts from the y-
    coordinate.  

    Attributes
    ----------
    max_columns : int
        Total number of columns available in the console.
    x : int
        Number of spaces the cursor is from the left. Default is 1.
    y : int
        Number of spaces the cursor is from the top. Default is 1.
    """

    __name__ = 'Canvas'
    __module__ = 'canvas'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        exc_tuple = (exc_type, exc_value, exc_traceback)
        if exc_tuple == (None, None, None):
            self.update_cursor_position()
            return

        traceback.print_exception(*exc_tuple)

    def __init__(self):

        self.max_columns = shutil.get_terminal_size().columns

        self.x = 1
        self.y = 1

    def update_cursor_position(self):
        """Updates the current cursor position.

        ``x`` and ``y`` will be set to new values depending on where the
        cursor is in the console.

        Note
        ----
        There are two different functions responsible for fetching the
        current cursor position. One is used on Windows machines while
        the other is used on Unix machines.
        """

        pos = utils.get_cursor_position()
        # Unix:
        if hasattr(pos, '__iter__'):
            self.y, self.x = pos
        # Windows:
        else:
            self.x = pos.X
            self.y = pos.Y

    def update_max_columns(self):
        """Updates the current number of columns available.

        If the user adjusts the width of their terminal, the number
        of maximum columns will obviously change as well. This function
        should be called when that occurs.
        """

        self.max_columns = shutil.get_terminal_size().columns
