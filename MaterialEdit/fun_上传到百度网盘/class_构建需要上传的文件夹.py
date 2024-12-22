"""构建需要上传的文件夹."""

from __future__ import annotations

import contextlib
import subprocess
import time
from pathlib import Path

import pyautogui
import pygetwindow

from MaterialEdit.fun_上传到百度网盘.class_上传单个文件 import UpOneFolderToBaiduWangPan
from MaterialEdit.fun_上传到百度网盘.def_获取指定窗口 import fun_获取指定窗口
from MaterialEdit.get_stem_num import get_path_num


class UpAllFolderToBaiduWangPan:
    """上传所有的素材文件夹到百度网盘."""

    win_width = pyautogui.size().width
    win_height = pyautogui.size().height

    def __init__(self, parent_path: str, start_stem: int, end_stem: int) -> None:
        """父文件夹 起始num 结束的num."""
        self.parent_path = parent_path
        self.start_stem = start_stem
        self.end_stem = end_stem

    def __fun_所有需要上传的文件夹(self) -> list[UpOneFolderToBaiduWangPan]:
        """获取所有需要上传的文件夹."""
        return [
            UpOneFolderToBaiduWangPan(folder=folder)
            for folder in Path(self.parent_path).iterdir()
            if folder.is_dir() and self.start_stem <= get_path_num(folder.stem) <= self.end_stem
        ]

    def __fun_打开百度网盘并移动到置顶位置(self) -> None:
        """置顶百度网盘，并且移动位置."""
        win = fun_获取指定窗口(window_title="百度网盘")
        if win:
            win.resizeTo(newWidth=int(self.win_width / 2), newHeight=1200)
            win.moveTo(newLeft=int(self.win_width / 2), newTop=0)
            win.activate()

    def __fun_打开资源管理器并移动到指定位置(self) -> None:
        """操作之前先置顶window资源管理器."""
        win = fun_获取指定窗口(window_title="文件资源管理器")
        if win is None:
            subprocess.run(args="explorer.exe", check=False)

        time.sleep(2)

        win = fun_获取指定窗口(window_title="文件资源管理器")
        if win:
            win.resizeTo(newWidth=int(self.win_width / 2), newHeight=1200)
            win.moveTo(newLeft=0, newTop=0)
            win.activate()

    def main(self) -> None:
        """遍历需要传输的文件夹开始操作."""
        self.__fun_打开百度网盘并移动到置顶位置()
        time.sleep(2)

        with contextlib.suppress(pygetwindow.PyGetWindowException):
            self.__fun_打开资源管理器并移动到指定位置()
            time.sleep(2)

        for folder_obj in self.__fun_所有需要上传的文件夹():
            folder_obj.main()


if __name__ == "__main__":
    up_obj = UpAllFolderToBaiduWangPan(
        parent_path=r"F:\饭桶设计\3000-3999",
        start_stem=3600,
        end_stem=3687,
    )
    up_obj.main()
