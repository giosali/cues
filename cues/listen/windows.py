# -*- coding: utf-8 -*-

"""
cues.listen.windows
===================

This module is for listening for keystrokes on Windows machines.
"""

try:
    import msvcrt  # pylint: disable=import-error
except ModuleNotFoundError:
    pass
from ctypes import Structure, byref, c_long, c_short, c_ushort
try:
    from ctypes import windll
except ImportError:
    pass

from . import ansi


def listen():
    key = ord(msvcrt.getch())

    if key == ansi.CTRL_C:
        raise KeyboardInterrupt

    elif key == ansi.ESC or key == ansi.NULL:
        key = ord(msvcrt.getch()) + 224

    return key


class COORD(Structure):
    _fields_ = [
        ('X', c_short),
        ('Y', c_short)
    ]


class SMALL_RECT(Structure):
    _fields_ = [
        ('Left', c_short),
        ('Top', c_short),
        ('Right', c_short),
        ('Bottom', c_short)
    ]


class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    _fields_ = [
        ('dwSize', COORD),
        ('dwCursorPosition', COORD),
        ('wAttributes', c_ushort),
        ('srWindow', SMALL_RECT),
        ('dwMaximumWindowSize', COORD)
    ]


def get_std_handle(designation: int):
    """
    Returns a windll.kernel32.GetStdHandle object.

    A designation of -10 == stdin
    A designation of -11 == stdout
    A designation of -12 == stderr
    """

    if not -12 <= designation <= -10:
        raise ValueError('Designation must be between -10 and -12')

    return windll.kernel32.GetStdHandle(c_long(designation))


def get_coord(x: int, y: int) -> COORD:
    """
    Instantiates and returns a COORD object.
    """

    if x < 0 or y < 0:
        raise ValueError(
            f'Coordinates cannot be less than 0: x = {x}, y = {y}')

    coord = COORD(x, y)
    return coord


def update_coord(coord: COORD, x: int = 0, y: int = 0):
    """
    Returns None. It simply modifies a given COORD object's X and Y member variables.
    Essentially, `coord` is treated as an output parameter.
    """

    if x:
        coord.X = x
    if y:
        coord.Y = y


def get_console_cursor_position(handle) -> CONSOLE_SCREEN_BUFFER_INFO.dwCursorPosition:
    """
    Returns a CONSOLE_SCREEN_BUFFER_INFO.dwCursorPosition object which contains the cursor's
    current location as coordinates.

    :param windll.kernel32.GetStdHandle handle: A handle.
    :rtype: CONSOLE_SCREEN_BUFFER_INFO.dwCursorPosition
    :returns: The cursor.
    """

    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    # Checks if console is open:
    if windll.kernel32.GetConsoleScreenBufferInfo(handle, byref(csbi)):
        return csbi.dwCursorPosition


def set_console_cursor_position(handle, coord: COORD):
    """
    Sets the cursor position in console.

    :param windll.kernel32.GetStdHandle handle: A handle.
    """

    windll.kernel32.SetConsoleCursorPosition(handle, coord)
