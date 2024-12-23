"""根据窗口标题 获取指定的窗口."""

from __future__ import annotations

import pygetwindow as gw
from pygetwindow import Win32Window


def fun_获取指定窗口(window_title: str) -> Win32Window | None:
    """根据窗口标题获取指定的窗口."""
    ws = gw.getWindowsWithTitle(title=window_title)
    if len(ws) > 0:
        return ws[0]

    return None
