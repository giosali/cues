"""
tests.test_color
================

A testing module for `cues.color`.
"""

import pathlib

import pytest

from cues import color


def test_make_colored():
    example_str_with_tags = '[red]This is text surrounded by red tags[/red], and this next portion is [yellow]yellow text surrounded by yellow tags[/yellow].'
    example_str_with_tags_expected_result = '\x1b[31mThis is text surrounded by red tags\x1b[0m, and this next portion is \x1b[33myellow text surrounded by yellow tags\x1b[0m.'

    example_str_with_graphics_tags = '[bold red]This is text surrounded by bold red tags[/bold red], and this next portion is [yellow]yellow text surrounded by yellow tags[/yellow].'
    example_str_with_graphics_tags_expected_result = '\x1b[1;31mThis is text surrounded by bold red tags\x1b[0m, and this next portion is \x1b[33myellow text surrounded by yellow tags\x1b[0m.'

    example_str_with_repeat_graphics_tags = '[bold red]This is text surrounded by bold red tags[/bold red], [bold red]this is more text surrounded by, you guessed it, bold red tags[/bold red], and this final portion is text surrounded by [underline cyan]text surrounded by underline cyan tags[/underline cyan].'
    example_str_with_repeat_graphics_tags_expected_result = '\x1b[1;31mThis is text surrounded by bold red tags\x1b[0m, \x1b[1;31mthis is more text surrounded by, you guessed it, bold red tags\x1b[0m, and this final portion is text surrounded by \x1b[4;36mtext surrounded by underline cyan tags\x1b[0m.'

    example_str_with_no_tags = 'This is some text without any tags in it.'
    example_str_with_no_tags_expected_result = 'This is some text without any tags in it.'

    example_str_with_tags_result = color.make_colored(
        example_str_with_tags)
    assert example_str_with_tags_result == example_str_with_tags_expected_result

    example_str_with_graphics_tags_result = color.make_colored(
        example_str_with_graphics_tags)
    assert example_str_with_graphics_tags_result == example_str_with_graphics_tags_expected_result

    example_str_with_repeat_graphics_tags_result = color.make_colored(
        example_str_with_repeat_graphics_tags)
    assert example_str_with_repeat_graphics_tags_result == example_str_with_repeat_graphics_tags_expected_result

    example_str_with_no_tags_result = color.make_colored(
        example_str_with_no_tags)
    assert example_str_with_no_tags_result == example_str_with_no_tags_expected_result
