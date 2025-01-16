"""get baidu download link"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import pyautogui
import pyperclip

from MaterialEdit.fun_自动操作.fun_窗口操作 import fun_获取窗口坐标
from MaterialEdit.fun_自动操作.fun_获取图片 import fun_获取图片

if TYPE_CHECKING:
    from collections.abc import Generator

pyautogui.PAUSE = 0.1


class AutoGetBaiDuShareLink:
    def __init__(self, start_stem: int, end_stem: int, parent_path: str) -> None:
        """初始化."""
        self.start_stem = start_stem
        self.end_stem = end_stem
        res = fun_获取窗口坐标("百度")
        if res is not None:
            self.baidu_position = res
        else:
            self.baidu_position = (0, 0, 1920, 1080)
        self.path_name = "网盘链接分享"
        self.parent_path = Path(parent_path)

    def fun_获取所有STEM(self) -> Generator[str, Any, None]:
        """获取所有需要下载的文件夹."""
        for in_file in self.parent_path.iterdir():
            if (
                in_file.is_dir()
                and self.start_stem <= int(in_file.stem) <= self.end_stem
            ):
                yield in_file.stem

    def fun_获取单个素材(self, material_id: str) -> str | None:
        """获取单个素材."""
        pyautogui.click(
            fun_获取图片("wodewangpan", self.path_name, self.baidu_position),
        )

        search_text = fun_获取图片("search_input", self.path_name, self.baidu_position)
        pyautogui.click(search_text)
        pyautogui.write(material_id)
        pyautogui.hotkey("enter")

        folder_xy = fun_获取图片("folder", self.path_name, self.baidu_position)

        if folder_xy is not None:
            pyautogui.rightClick(
                fun_获取图片("folder", self.path_name, self.baidu_position),
            )
            pyautogui.click(
                fun_获取图片("share_button", self.path_name, self.baidu_position),
            )
            pyautogui.click(
                fun_获取图片("yongjiuyouxiao", self.path_name, self.baidu_position),
            )
            pyautogui.click(
                fun_获取图片("chuangjian", self.path_name, self.baidu_position),
            )
            pyautogui.click(fun_获取图片("guanbi", self.path_name, self.baidu_position))

            return pyperclip.paste()

        return None

    @staticmethod
    def fun_处理返回的本文(material_id: str, text: str) -> str:
        """处理返回的本文."""
        text = material_id + "\t" + '"' + "\n".join(text.split("\n")[0:-2]) + '"\n\n'
        return text.replace(" ", "")

    def run(self) -> None:
        """运行."""
        pyautogui.sleep(3)

        text_file = Path.home() / "Desktop" / "output.txt"
        text_file.write_text("")

        with text_file.open("a+") as f:
            for material_id in self.fun_获取所有STEM():
                text = self.fun_获取单个素材(material_id=material_id)
                if text is not None:
                    text = self.fun_处理返回的本文(material_id, text)
                    f.write(text)
