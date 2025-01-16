"""windows窗口操作."""

from __future__ import annotations

import contextlib
import ctypes
import ctypes.wintypes
from typing import Any

import win32gui


def get_window_pos(hwnd: int) -> tuple[int, int, int, int] | None:
    """获取窗口坐标."""
    with contextlib.suppress(OSError):
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        rect = ctypes.wintypes.RECT()
        f(
            ctypes.wintypes.HWND(hwnd),
            ctypes.wintypes.DWORD(9),
            ctypes.byref(rect),
            ctypes.sizeof(rect),
        )
        return rect.left, rect.top, rect.right, rect.bottom

    return None


def fun_获取窗口坐标(windows_name: str) -> tuple[int, int, int, int] | None:
    """根据标题获取窗口坐标."""
    win_list: list[Any] = []
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), win_list)

    for win in win_list:
        title = win32gui.GetWindowText(win)

        if windows_name in title:
            res = get_window_pos(win)
            if res is not None:
                left, top, right, bottom = res
                return left, top, right, bottom

    return None


def fun_窗口置顶(windows_name: str) -> None:
    """根据窗口标题置顶窗口."""
    win_list: list[Any] = []
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), win_list)

    for win in win_list:
        title = win32gui.GetWindowText(win)
        if windows_name in title:
            win32gui.SetForegroundWindow(win)
            return
