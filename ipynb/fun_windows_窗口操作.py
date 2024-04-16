import ctypes
from pathlib import Path
import pyautogui
import win32com
import win32com.client
import win32gui
from PIL import Image


def fun_窗口置顶(windows_name: str):
    win_list = []
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), win_list)

    shell = win32com.client.Dispatch("WScript.Shell")

    for win in win_list:
        title = win32gui.GetWindowText(win)
        # print(title)
        if windows_name in title:
            shell.SendKeys("%")
            win32gui.SetForegroundWindow(win)
            break


def get_window_pos(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        rect = ctypes.wintypes.RECT()
        f(ctypes.wintypes.HWND(hwnd), ctypes.wintypes.DWORD(9), ctypes.byref(rect), ctypes.sizeof(rect))
        return rect.left, rect.top, rect.right, rect.bottom
    except WindowsError as e:
        raise e


def fun_获取窗口坐标(windows_name: str):
    win_list = []
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), win_list)

    for win in win_list:
        title = win32gui.GetWindowText(win)
        # print(title)
        if windows_name in title:
            l, t, r, b = get_window_pos(win)
            return l, t, r, b


def fun_查找图片坐标(image_name: str):
    im_path = Path(f"./IMAGE/BAIDU/{image_name}.png")
    position = fun_获取窗口坐标("欢迎使用百度网盘")
    print(position)
    if im_path.exists() is False:
        raise IndexError("图片不存在")

    im = Image.open(im_path.absolute())
    return pyautogui.locateOnScreen(im, region=position, grayscale=True, minSearchTime=15)
