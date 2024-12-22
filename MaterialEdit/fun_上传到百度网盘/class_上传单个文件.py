"""使用pyautogui上传单个文件."""

import time
from pathlib import Path

import pyautogui
import pyperclip

from MaterialEdit.fun_上传到百度网盘.def_获取指定窗口 import fun_获取指定窗口

pyautogui.PAUSE = 2


class UpOneFolderToBaiduWangPan:
    def __init__(
        self,
        folder: Path,
    ) -> None:
        """需要上传的文件夹 文件夹管理器窗口坐标 网盘APP窗口坐标."""
        self.folder = folder

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
        """点击左侧的文件夹 移动到百度网盘.

        1.点击 click
        2.移动 holdclick
        3.释放
        """

    def main(self) -> None:
        """开始操作."""
        self.__fun_激活资源管理器()
        time.sleep(2)
        self.__fun_地址栏输入文件夹()
        self.__移动文件夹()


if __name__ == "__main__":
    up_bd = UpOneFolderToBaiduWangPan(folder=Path(r"F:\泡泡素材\2000-2999\2880"))
    up_bd.main()
