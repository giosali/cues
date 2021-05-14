"""
cues.color
==========

A module that is responsible for bringing color to Cue objects.
"""
import re


class Color:
    """Brings color to the console.

    Color objects are intended to color str objects by using ANSI color
    codes.

    Parameters
    ----------
    color : str
        A str object indicating which color to use.
    """

    __name__ = 'Color'
    __module__ = 'prompts'

    RESET = '\x1b[0m'

    GRAPHICS = {
        'bold': '\x1b[1',
        'dim': '\x1b[2',
        'italic': '\x1b[3',
        'underline': '\x1b[4',
        'strikethrough': '\x1b[9'
    }

    FOREGROUND_COLORS = {
        'black': '\x1b[30m',
        'red': '\x1b[31m',
        'green': '\x1b[32m',
        'yellow': '\x1b[33m',
        'blue': '\x1b[34m',
        'magenta': '\x1b[35m',
        'cyan': '\x1b[36m',
        'white': '\x1b[37m',
        # =========256=========
        'aquamarine': '\x1b[38;5;123m',
        'brown': '\x1b[38;5;130m',
        'darkgray': '\x1b[38;5;238m',
        'darkgrey': '\x1b[38;5;238m',
        'gray': '\x1b[38;5;246m',
        'grey': '\x1b[38;5;246m',
        'greenyellow': '\x1b[38;5;154m',
        'lightslateblue': '\x1b[38;5;105m',
        'lightsteelblue': '\x1b[38;5;147m',
        'pink': '\x1b[38;5;212m',
        'skyblue': '\x1b[38;5;117m',
        'thistle': '\x1b[38;5;225m',
        'violet': '\x1b[38;5;177m'
    }

    BACKGROUND_COLORS = {
        'black': '\x1b[40m',
        'red': '\x1b[41m',
        'green': '\x1b[42m',
        'yellow': '\x1b[43m',
        'blue': '\x1b[44m',
        'magenta': '\x1b[45m',
        'cyan': '\x1b[46m',
        'white': '\x1b[47m',
    }

    def __init__(self, color: str):
        """Inits a Color class with `color`.
        """

        self._color = color.strip().lower()


def make_colored(text: str) -> str:
    """Returns a str object with ANSI color codes.

    Takes a str object that contains color tags (e.g., 
    "[red]Hi[/red]") and replaces them with ANSI color
    codes.

    Parameters
    ----------
    text : str
        A str object that may or may not contain color tags.

    Returns
    -------
    text : str
        The same str object but with the color tags replaced with
        ANSI color codes.
    """

    color_tag_pattern = re.compile(r'\[\/?\w+ ?\w+\]')

    color_tags = re.findall(color_tag_pattern, text)
    if color_tags:
        text = replace_tags_with_color_codes(text, color_tags)

    return text


def replace_tags_with_color_codes(text: str, tags: list) -> str:
    """Replaces color tags in a str object with ANSI color codes.

    Parameters
    ----------
    text : str
        A str object that may or may not contain color tags.
    tags : list
        A list object that contains the color tags in the `text` parameter.

    Returns
    -------
    text : str
        The same str object but with the color tags replaced with
        ANSI color codes.
    """

    color_str_pattern = re.compile(r'\/?\w+ ?\w+')

    for tag in tags:
        tag_text = re.search(color_str_pattern, tag).group()
        # Split the tag portion into different segments:
        split_tag_text = tag_text.split()

        # Refresh replacement string:
        tag_str_repl = ''
        for elem in split_tag_text:
            if elem.startswith('/'):
                tag_str_repl = Color.RESET
                break

            tag_str_repl += Color.GRAPHICS.get(elem, '')
            # If the replacement has a graphics code, modify the color code:
            if tag_str_repl:
                tag_str_repl += Color.FOREGROUND_COLORS.get(
                    elem, '').replace('\x1b[', ';')
            # otherwise:
            else:
                tag_str_repl += Color.FOREGROUND_COLORS.get(elem, '')

        joined_tags = ' '.join(split_tag_text)

        text = re.sub(re.compile(
            r'\[{}\]'.format(joined_tags)), tag_str_repl, text)

    return text
