"""
cues.listen.unix
================

This module is for listening for keystrokes on macOS/Linux machines.
"""

import select
import sys
try:
    import termios  # pylint: disable=import-error
except ModuleNotFoundError:
    pass
try:
    import tty
except ModuleNotFoundError:
    pass

from . import ansi


def listen():
    fd = sys.stdin.fileno()  # File descriptor
    old = termios.tcgetattr(fd)  # Necessary for restoring tty attributes

    try:
        # Allows user to manipulate program with interrupt/quit characters.
        # See 'https://people.csail.mit.edu/jaffer/scm/Terminal-Mode-Setting.html' for
        # more info.
        tty.setcbreak(fd)

        while True:
            if is_data():
                key = sys.stdin.read(1)

                if key == ansi.ESC_CODE:
                    key = sys.stdin.read(2)

                    return key

                return ord(key)
    finally:
        # Old tty attributes restored:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def is_data() -> bool:
    return select.select([sys.stdin.fileno()], [], [], 0) == ([sys.stdin.fileno()], [], [])
