import os
import time
from collections.abc import Generator
from pathlib import Path

import pyautogui
from tqdm import tqdm

from ..get_stem_num import get_path_num
from .fun_判断文件夹是否为空 import fun_判断是否为空文件夹
from .fun_窗口操作 import fun_窗口置顶, fun_获取窗口坐标
from .fun_获取图片 import fun_获取图片

pyautogui.PAUSE = 0.5


class AutoUploadMaterialToBaiduYun:
    def __init__(self, parent_path: str, start_stem: int) -> None:
        """自动上传文件到百度网盘

        :param str parent_path: 父文件夹
        :param int start_stem: 起始数字
        """
        self.parent_path = Path(parent_path)
        self.start_stem = start_stem

    def fun_遍历文件夹(self) -> Generator[Path]:
        """遍历所有需要上传的文件夹."""
        for in_file in self.parent_path.iterdir():
            if in_file.is_dir() and get_path_num(in_file.stem) >= self.start_stem:
                yield in_file

    @staticmethod
    def fun_上传单个文件夹(folder_path: Path):
        print(folder_path)
        path_name = "上传到网盘"
        os.startfile(folder_path)
        position = fun_获取窗口坐标(folder_path.name)
        fun_窗口置顶(folder_path.name)

        x, y = fun_获取图片("name", path_name, position)
        pyautogui.moveTo((x, y + 45))
        pyautogui.click()
        pyautogui.keyDown("shift")
        pyautogui.rightClick()
        pyautogui.keyUp("shift")

        time.sleep(2)
        pyautogui.click(fun_获取图片("up_to_baidu_button", path_name, position))
        fun_窗口置顶(folder_path.name)
        pyautogui.hotkey("ctrl", "w")

        time.sleep(1)

    def run(self):
        for in_path in tqdm(
            list(self.fun_遍历文件夹()),
            ncols=100,
            desc="上传到百度网盘\t",
        ):
            if fun_判断是否为空文件夹(in_path) is True:
                print(in_path)
                self.fun_上传单个文件夹(folder_path=in_path)
