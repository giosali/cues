"""
cues.utils
==========

This module contains useful, general functions.
"""

import math
import platform
import sys

from .listen import ansi, windows, unix


def is_windows() -> bool:
    """Return whether the user is using a Windows machine or not.

    Returns
    -------
    :rtype: bool
    """

    if platform.system() == 'Windows':
        return True
    return False


def get_keys() -> dict:
    """Returns a dict object contains keys based on OS.

    Returns
    -------
    :rtype: dict
    """
    keys = {
        'n': ansi.N_CODE,
        'N': ansi.N_SHIFT_CODE,
        'y': ansi.Y_CODE,
        'Y': ansi.Y_SHIFT_CODE,
    }

    if is_windows():
        keys.update({
            'up': ansi.UP,
            'right': ansi.RIGHT,
            'down': ansi.DOWN,
            'left': ansi.LEFT,

            'enter': ansi.ENTER,
            'backspace': ansi.BACKSPACE,
        })
    # Unix:
    else:
        keys.update({
            'up': ansi.NO_ESC_UP,
            'right': ansi.NO_ESC_RIGHT,
            'down': ansi.NO_ESC_DOWN,
            'left': ansi.NO_ESC_LEFT,

            'enter': ansi.ENTER_CTRL_CODE,
            'backspace': ansi.BACKSPACE_CTRL_CODE,
        })

    return keys


def get_num_digits(n: int) -> int:
    """Returns the number of digits in an integer.

    Returns
    -------
    :rtype: int
    """

    num_digits = int(math.log10(n)) + 1
    return num_digits


def get_half(n: int) -> int:
    """Gets the half point of an integer

    Parameters
    ----------
    n : int
        The number to divide in half.

    Returns
    -------
    :rtype: int
    """

    return math.ceil(n / 2)


def get_listen_function() -> windows.listen or unix.listen:
    """Returns appropriate listening function based on OS.

    Returns
    -------
    :rtype: function
    """
    if is_windows():
        return windows.listen
    return unix.listen
