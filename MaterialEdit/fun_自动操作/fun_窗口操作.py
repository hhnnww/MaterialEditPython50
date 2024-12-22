"""windows窗口操作."""

from __future__ import annotations

import ctypes
from typing import Any

import win32gui


def get_window_pos(hwnd):  # noqa: ANN001, ANN201
    """获取窗口坐标."""
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        rect = ctypes.wintypes.RECT()
        f(
            ctypes.wintypes.HWND(hwnd),
            ctypes.wintypes.DWORD(9),
            ctypes.byref(rect),
            ctypes.sizeof(rect),
        )
        return rect.left, rect.top, rect.right, rect.bottom  # noqa: TRY300
    except OSError as e:
        return e


def fun_获取窗口坐标(windows_name: str) -> tuple[int, int, int, int] | None:
    """根据标题获取窗口坐标."""
    win_list: list[Any] = []
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), win_list)

    for win in win_list:
        title = win32gui.GetWindowText(win)

        if windows_name in title:
            left, top, right, bottom = get_window_pos(win)
            return left, top, right, bottom

    return None


def fun_窗口置顶(windows_name: str) -> None:
    """根据窗口标题置顶窗口."""
    win_list: list[Any] = []
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), win_list)

    for win in win_list:
        title = win32gui.GetWindowText(win)
        print(title)
        if windows_name in title:
            win32gui.SetForegroundWindow(win)
            return
