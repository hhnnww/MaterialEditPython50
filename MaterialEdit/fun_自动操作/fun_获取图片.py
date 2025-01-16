"""获取图片"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pyautogui
from PIL import Image

if TYPE_CHECKING:
    from pyscreeze import Point


def fun_获取图片(
    img_name: str,
    path_name: str,
    position: tuple[int, int, int, int],
) -> None | Point:
    """Pyautogui 自动获取图片的位置，如果不存在则等待查找"""
    image_root_path = Path(__file__).parent / "img" / path_name
    img_path = image_root_path / (img_name + ".png")

    if img_path.exists() is False:
        msg = f"路径不存在 {img_path}"
        raise IndexError(msg)

    num = 1
    max_wait = 5
    with Image.open(img_path.as_posix()) as im:
        while (
            pyautogui.locateCenterOnScreen(
                image=im,
                minSearchTime=15,
                grayscale=True,
                region=position,
            )
            is None
        ):
            pyautogui.sleep(1)
            num += 1

            if num == max_wait:
                return None

        return pyautogui.locateCenterOnScreen(
            image=im,
            minSearchTime=15,
            grayscale=True,
            region=position,
        )
