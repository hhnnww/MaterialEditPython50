"""构建需要上传的文件夹."""

from __future__ import annotations

import contextlib
import subprocess
import time
from pathlib import Path

import pyautogui
import pygetwindow
from PIL import Image

from MaterialEdit.get_stem_num import get_path_num
from route_上传到百度网盘.class_上传单个文件 import UpOneFolderToBaiduWangPan
from route_上传到百度网盘.def_获取指定窗口 import fun_获取指定窗口


class UpAllFolderToBaiduWangPan:
    """上传所有的素材文件夹到百度网盘."""

    win_width = pyautogui.size().width
    win_height = pyautogui.size().height

    def __init__(
        self,
        parent_path: str,
        start_stem: int,
        end_stem: int = 99999,
    ) -> None:
        """父文件夹 起始num 结束的num."""
        self.parent_path = parent_path
        self.start_stem = start_stem
        self.end_stem = end_stem

    def __fun_所有需要上传的文件夹(self) -> list[UpOneFolderToBaiduWangPan]:
        """获取所有需要上传的文件夹."""
        exp_point = self.__fun_获取资源管理器的文件夹坐标()
        baidu_pint = self.__fun_获取网盘的坐标()
        return [
            UpOneFolderToBaiduWangPan(
                folder=folder,
                exp_point=exp_point,
                baidu_point=baidu_pint,
            )
            for folder in Path(self.parent_path).iterdir()
            if folder.is_dir()
            and self.start_stem <= get_path_num(stem=folder.stem) <= self.end_stem
        ]

    def __fun_打开百度网盘并移动到置顶位置(self) -> None:
        """置顶百度网盘，并且移动位置."""
        win = fun_获取指定窗口(window_title="百度网盘")
        if win:
            win.activate()
            time.sleep(2)
            win.resizeTo(
                newWidth=int(self.win_width / 2),
                newHeight=int(self.win_height / 2),
            )
            win.moveTo(newLeft=int(self.win_width / 2), newTop=0)
            time.sleep(2)

    def __fun_打开资源管理器并移动到指定位置(self) -> None:
        """操作之前先置顶window资源管理器."""
        subprocess.run(args="explorer.exe F:\\", check=False)
        time.sleep(2)

        win = fun_获取指定窗口(window_title="文件资源管理器")
        if win:
            win.activate()
            time.sleep(2)
            win.resizeTo(
                newWidth=int(self.win_width / 2),
                newHeight=int(self.win_height / 2),
            )
            win.moveTo(newLeft=0, newTop=0)
            time.sleep(2)

    @staticmethod
    def __fun_隐藏当前所有窗口() -> None:
        pyautogui.hotkey("win", "d")

    @staticmethod
    def __fun_获取资源管理器的文件夹坐标() -> pyautogui.Point:
        """获取文件夹地址的坐标."""
        with Image.open((Path(__file__).parent / "img" / "name.png").as_posix()) as im:
            return pyautogui.locateCenterOnScreen(image=im)  # type: ignore

    @staticmethod
    def __fun_获取网盘的坐标() -> pyautogui.Point:
        """获取网盘目标坐标."""
        return pyautogui.Point(x=2500, y=370)

    def main(self) -> None:
        """开始上传."""
        self.__fun_隐藏当前所有窗口()
        time.sleep(2)

        with contextlib.suppress(pygetwindow.PyGetWindowException):
            self.__fun_打开百度网盘并移动到置顶位置()

        with contextlib.suppress(pygetwindow.PyGetWindowException):
            self.__fun_打开资源管理器并移动到指定位置()

        for folder_obj in self.__fun_所有需要上传的文件夹():
            folder_obj.main()
