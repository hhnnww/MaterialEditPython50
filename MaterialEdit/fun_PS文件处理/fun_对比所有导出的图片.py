from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from pyzbar import pyzbar

from MaterialEdit.fun_图片编辑.fun_删除图片边框.fun_删除图片边框 import fun_删除图片边框


def fun_cv2_to_pil(img: np.ndarray) -> Image.Image:
    """CV2转PIL"""
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))


def fun_pil_to_cv2(img: Image.Image) -> np.ndarray:
    """PIL转CV2"""
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA)


def fun_打开图片(
    img_path: str,
) -> np.ndarray:
    """打开图片"""
    return cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)


def fun_所有广告图片() -> list[Path]:
    """获取所有广告图片"""
    ad_pic_path = Path(__file__).parent / "广告图片"
    return [
        in_file
        for in_file in ad_pic_path.iterdir()
        if in_file.is_file() and in_file.suffix.lower() in [".png"]
    ]


def fun_图片边缘(img: np.ndarray) -> np.ndarray:
    """获取图片边缘"""
    img = cv2.resize(img.copy(), (100, 100), interpolation=cv2.INTER_NEAREST)
    img = cv2.Canny(img, 3, 30)
    rec, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    return img


def fun_获取所有白色像素(img: np.ndarray) -> int:
    """获取所有白色像素"""
    white = np.bincount(img.ravel())
    if len(white) == 1:
        return 0
    return white.item(-1)


def fun_判断比例(img_1: np.ndarray, img_2: np.ndarray) -> bool:
    """判断比例"""
    radio_1 = img_1.shape[0] / img_1.shape[1]
    radio_2 = img_2.shape[0] / img_2.shape[1]
    abs_radio = abs(radio_1 - radio_2)
    diff = 0.1
    return abs_radio < diff


def fun_叠加差异(img_1: np.ndarray, img_2: np.ndarray) -> bool:
    """叠加差异"""
    img_1_pil = fun_cv2_to_pil(img_1)
    img_1_pil = fun_删除图片边框(img_1_pil)
    img_1 = fun_pil_to_cv2(img_1_pil)

    im_1 = fun_图片边缘(img_1.copy())
    im_2 = fun_图片边缘(img_2.copy())

    diff = cv2.absdiff(im_1, im_2)
    diff_white = fun_获取所有白色像素(diff)

    # 如果差异完全无白色
    # 就是完全相同的图片
    if diff_white == 0:
        return True

    # 如果差异小于最小的 0.3
    # 至少大概率相同
    im_1_white = fun_获取所有白色像素(im_1)
    im_2_white = fun_获取所有白色像素(im_2)
    diff = 200
    return bool(
        diff_white < min([im_1_white, im_2_white]) * 0.8
        and abs(im_1_white - im_2_white) < diff,
    )


def fun_单个图片对比(img_1: np.ndarray, img_2: np.ndarray) -> bool:
    """单个图片对比"""
    if len(pyzbar.decode(img_1)) > 0:
        return True

    return bool(
        fun_判断比例(img_1, img_2) is True and fun_叠加差异(img_1, img_2) is True,
    )


def run_对比所有图片(img: np.ndarray, ad_img_list: list) -> bool:
    """对比所有图片"""
    for ad_img in ad_img_list:
        if fun_单个图片对比(img_1=img, img_2=ad_img) is True:
            return True

    return False
