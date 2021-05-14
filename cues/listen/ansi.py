"""
cues.listen.ansi
================

This module contains information for ANSI escape codes.
"""

# Keyboard strings:

NULL = 0  # Null character

ESC = 224  # Ordinal number for the ESC key:

CTRL_C = 3  # Ordinal number for CTRL + C:

SHIFT = 224
UP = 72 + SHIFT  # Ordinal number for the up arrow key / Windows
RIGHT = 77 + SHIFT  # Ordinal number for the right arrow key / Windows
DOWN = 80 + SHIFT  # Ordinal number for the down arrow key / Windows
LEFT = 75 + SHIFT  # Ordinal number for the left arrow key / Windows

ENTER = 13  # Ordinal number for the enter key / Windows
ENTER_CTRL_CODE = 10  # Ordinal number for the enter key (CTRL + code) / Unix

BACKSPACE = 8  # Ordinal number for the backspace key / Windows
BACKSPACE_CTRL_CODE = 127  # Backspace key (CTRL + code) / Unix

Y_CODE = 121
Y_SHIFT_CODE = 89
N_CODE = 110
N_SHIFT_CODE = 78

# Cursor controls:

UP_ONE = '\x1b[1A'  # Moves cursor up one line

ESC_CODE = '\x1b'  # Standard hexadecimal escape code for ESC

NO_ESC_UP = '[A'  # ESC code sequence for up arrow key without ESC / Unix
NO_ESC_DOWN = '[B'  # ESC code sequence for down arrow key without ESC / Unix
NO_ESC_RIGHT = '[C'  # ESC code sequence for right arrow key without ESC / Unix
NO_ESC_LEFT = '[D'  # ESC code sequence for left arrow key without ESC / Unix

MOVE_UP = '\x1b[{}A'  # Moves cursor up # of times
MOVE_DOWN = '\x1b[{}B'  # Moves cursor down # of times
MOVE_RIGHT = '\x1b[{}C'  # Moves cursor to the right # of times
MOVE_LEFT = '\x1b[{}D'  # Moves cursor to the left # of times


# Erase functions:

CLEAR_LINE = '\x1b[K'  # Clears the current line


# Set mode:

HIDE_CURSOR = '\x1b[?25l'
SHOW_CURSOR = '\x1b[?25h'
