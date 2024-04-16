from ...type import _COLOR, _FONT_NAME, _FONT_WEIGHT
from ..fun_单行文字转图片.fun_单行文字转图片 import fun_单行文字转图片
from ..fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from .fun_文字换行 import fun_文字换行


def fun_制作多行本文(
    text: str,
    line_max_number: int,
    spacing: int,
    chinese_font_name: _FONT_NAME,
    english_font_name: _FONT_NAME,
    font_weight: _FONT_WEIGHT,
    font_size: int,
    fill_color: _COLOR,
    background_color: _COLOR,
    en_size_expand_ratio: float = 1.2,
):
    text_list = fun_文字换行(text=text, line_max_number=line_max_number)

    text_pil_list = []
    for t in text_list:
        im = fun_单行文字转图片(
            text=t,
            chinese_font_name=chinese_font_name,
            english_font_name=english_font_name,
            font_weight=font_weight,
            font_size=font_size,
            fill_color=fill_color,
            background_color=background_color,
            en_size_expand_ratio=en_size_expand_ratio,
        )

        text_pil_list.append(im)

    im = fun_图片竖向拼接(
        image_list=text_pil_list,
        spacing=spacing,
        align_item="start",
        background_color=background_color,
    )

    return im
