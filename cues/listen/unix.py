# -*- coding: utf-8 -*-

"""
cues.listen.unix
================

This module is for listening for keypresses on macOS/Linux machines.
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

        key = get_key()
        return key
    finally:
        # Old tty attributes restored:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def get_key():
    while True:
        if is_data():
            key = sys.stdin.read(1)

            if key == ansi.ESC_CODE:
                key = sys.stdin.read(2)
                return key

            return ord(key)


def is_data() -> bool:
    return select.select([sys.stdin.fileno()], [], [], 0) == ([sys.stdin.fileno()], [], [])


def listen_for_pos():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        # TCSANOW: change should occur immediately:
        tty.setcbreak(fd, termios.TCSANOW)

        pos = get_pos()
        return pos

    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old)


def get_pos() -> str:
    buffer = ''
    sys.stdout.write(ansi.CURSOR_POS)
    sys.stdout.flush()

    while True:
        buffer += sys.stdin.read(1)
        if buffer.endswith('R'):
            return buffer
