import ctypes
import win32gui


def get_window_pos(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        rect = ctypes.wintypes.RECT()
        f(
            ctypes.wintypes.HWND(hwnd),
            ctypes.wintypes.DWORD(9),
            ctypes.byref(rect),
            ctypes.sizeof(rect),
        )
        return rect.left, rect.top, rect.right, rect.bottom
    except WindowsError as e:
        raise e


def fun_获取窗口坐标(windows_name: str):
    win_list = []
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), win_list)

    for win in win_list:
        title = win32gui.GetWindowText(win)

        if windows_name in title:
            l, t, r, b = get_window_pos(win)
            return l, t, r, b


def fun_窗口置顶(windows_name: str):
    win_list = []
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), win_list)

    for win in win_list:
        title = win32gui.GetWindowText(win)
        print(title)
        if windows_name in title:
            win32gui.SetForegroundWindow(win)
            break
