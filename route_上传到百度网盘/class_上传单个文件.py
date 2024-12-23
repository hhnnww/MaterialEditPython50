"""使用pyautogui上传单个文件."""

import time
from pathlib import Path

import pyautogui
import pyperclip

from route_上传到百度网盘.def_获取指定窗口 import fun_获取指定窗口

pyautogui.PAUSE = 1


class UpOneFolderToBaiduWangPan:
    def __init__(self, folder: Path, exp_point: pyautogui.Point, baidu_point: pyautogui.Point) -> None:
        """需要上传的文件夹 文件夹管理器窗口坐标 网盘APP窗口坐标."""
        self.folder = folder
        self.exp_point = exp_point
        self.baidu_point = baidu_point

    @staticmethod
    def __fun_激活资源管理器() -> None:
        """运行前先激活资源管理器."""
        win = fun_获取指定窗口(window_title="文件资源管理器")
        if win:
            win.activate()

    def __fun_地址栏输入文件夹(self) -> None:
        """资源管理器的地址栏输入文件夹地址."""
        pyperclip.copy(self.folder.as_posix())
        pyautogui.hotkey("alt", "d")
        pyautogui.hotkey("delete")
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")

    def __移动文件夹(self) -> None:
        """拖动素材文件夹到百度网盘.

        1.点击 click
        2.移动 holdclick
        """
        pyautogui.leftClick(x=self.exp_point.x, y=self.exp_point.y + 50)
        time.sleep(2)
        pyautogui.dragTo(x=self.baidu_point.x, y=self.baidu_point.y, duration=1)

    def main(self) -> None:
        """开始操作."""
        self.__fun_激活资源管理器()
        time.sleep(1)
        self.__fun_地址栏输入文件夹()
        time.sleep(2)
        self.__移动文件夹()
