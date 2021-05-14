"""
tests.test_windows
==================

A testing module for `cues.listen.windows`.
"""

import platform
try:
    import msvcrt
except ModuleNotFoundError:
    pass
from ctypes import Structure, byref, c_long, c_short, c_ushort
try:
    from ctypes import windll
except ImportError:
    pass

import pytest

import cues.listen.ansi as ansi
import cues.listen.windows as windows


@pytest.mark.skipif(platform.system() != 'Windows', reason='OS must be Windows')
def test_listen(monkeypatch):
    monkeypatch.setattr('msvcrt.getch', lambda: ansi.CTRL_C)

    key = msvcrt.getch()
    assert key == ansi.CTRL_C


@pytest.mark.skipif(platform.system() != 'Windows', reason='OS must be Windows')
def test_get_std_handle():
    # testing positive number:
    with pytest.raises(ValueError):
        windows.get_std_handle(1)
    # testing lower bound - 1:
    with pytest.raises(ValueError):
        windows.get_std_handle(-9)
    # testing upper bound + 1:
    with pytest.raises(ValueError):
        windows.get_std_handle(-13)

    # make sure handles match
    assert windows.get_std_handle(
        -11) == windll.kernel32.GetStdHandle(c_long(-11))


@pytest.mark.skipif(platform.system() != 'Windows', reason='OS must be Windows')
def test_get_coord():
    # coordinates must be greater than or equal to 0:
    with pytest.raises(ValueError):
        windows.get_coord(-1, -1)
    with pytest.raises(ValueError):
        windows.get_coord(0, -1)
    with pytest.raises(ValueError):
        windows.get_coord(-1, 0)

    # make sure coords match:
    x_val = 3
    y_val = 5
    windows_get_coord_obj = windows.get_coord(x_val, y_val)
    test_windows_coord_obj = windows.COORD(x_val, y_val)
    assert windows_get_coord_obj.X == test_windows_coord_obj.X
    assert windows_get_coord_obj.Y == test_windows_coord_obj.Y


@pytest.mark.skipif(platform.system() != 'Windows', reason='OS must be Windows')
def test_update_coord():
    x_val = 3
    y_val = 5
    dummy_x = 2
    dummy_y = 1
    windows_get_coord_obj = windows.get_coord(x_val, y_val)
    windows.update_coord(windows_get_coord_obj, dummy_x, dummy_y)
    assert windows_get_coord_obj.X == dummy_x
    assert windows_get_coord_obj.Y == dummy_y

    new_dummy_x = 3
    windows.update_coord(windows_get_coord_obj, new_dummy_x)
    assert windows_get_coord_obj.X == new_dummy_x
    # This shouldn't change since we didn't supply a y value to update_coord:
    assert windows_get_coord_obj.Y == dummy_y


# @pytest.mark.skipif(platform.system() != 'Windows', reason='OS must be Windows')
# def test_get_console_cursor_position():
#     stdout_handle = windows.get_std_handle(-11)

#     # Note: This throws an AssertionError if you use pytest but don't include the
#     # -s flag to capture stdout output:
#     assert windows.get_console_cursor_position(stdout_handle) is not None
