"""预览图水印"""

from pathlib import Path
from typing import Literal

from PIL import Image


def fun_单个预览图效果图水印(
    shop_name: str,
    cate: Literal["xgt", "ylt"],
) -> Image.Image:
    """根据店铺名称和类别生成单个预览图或效果图的水印。

    参数:
        shop_name (str): 店铺名称，用于生成文件名。
        cate (Literal["xgt", "ylt"]): 图片类别，"xgt" 表示效果图，"ylt" 表示预览图。
    返回:
        Image.Image: 打开的图片对象。
    异常:
        FileNotFoundError: 如果指定的图片文件不存在。
        ValueError: 如果传入的类别不在允许的范围内。
    """
    parent_path = Path(__file__)
    return Image.open(parent_path.parent / f"{shop_name}-{cate}.png")
