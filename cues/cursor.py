"""
cues.cursor
==========

This module moves the cursor in the console by using ANSI escape codes.
"""

import sys

from . import color as color_
from .listen import ansi


def hide():
    """Hides cursor in the console.
    """

    write(ansi.HIDE_CURSOR)


def show():
    """Restores cursor in the console.
    """

    write(ansi.SHOW_CURSOR)


def clear(lines: int):
    fmt = '{}{}'
    for _ in range(lines):
        write(fmt.format(ansi.UP_ONE, ansi.CLEAR_LINE))


def move(x: int = 0, y: int = 0):
    statement = ''
    if y:
        if y < 0:
            down = ansi.MOVE_DOWN.format(abs(y))
            statement += down

        else:
            up = ansi.MOVE_UP.format(y)
            statement += up

    if x:
        if x < 0:
            left = ansi.MOVE_LEFT.format(abs(x))
            statement += left

        else:
            right = ansi.MOVE_RIGHT.format(x)
            statement += right
    write(statement)


def write(text: str, color=False):
    if color:
        text = color_.make_colored(text)

    sys.stdout.write(text)
    sys.stdout.flush()
