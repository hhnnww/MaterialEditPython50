from pathlib import Path
from typing import Any

import pyautogui
from PIL import Image


def fun_获取图片(img_name: str, path_name: str, position: Any):
    """
    pyautogui 自动获取图片的位置，如果不存在则等待查找
    :param img_name: 图片名称
    :param path_name: 路径名称
    :param position: 查找位置
    :return:
    """
    # print(img_name, path_name, position)

    image_root_path = Path(__file__).parent / "img" / path_name
    img_path = image_root_path / (img_name + ".png")

    if img_path.exists() is False:
        raise IndexError(f"路径不存在 {img_path}")

    num = 1
    with Image.open(img_path.as_posix()) as im:
        while (
            pyautogui.locateCenterOnScreen(
                image=im, minSearchTime=15, grayscale=True, region=position
            )
            is None
        ):
            print("找不到图片")
            pyautogui.sleep(1)
            num += 1

            if num == 5:
                return None

        return pyautogui.locateCenterOnScreen(
            image=im, minSearchTime=15, grayscale=True, region=position
        )
