from PIL import Image, ImageDraw, ImageFont

from MaterialEdit.fun_图片编辑.fun_删除图片边框.fun_删除图片边框 import fun_删除图片边框
from MaterialEdit.fun_图片编辑.fun_单行文字转图片.fun_判断是否是英文 import fun_是英文
from MaterialEdit.fun_图片编辑.fun_单行文字转图片.fun_获取字体 import fun_获取字体
from MaterialEdit.fun_图片编辑.fun_单行文字转图片.fun_计算一行文字的宽度和高度 import (
    fun_计算一行文字的宽度和高度,
)
from MaterialEdit.fun_图片编辑.fun_单行文字转图片.fun_计算单个文字的尺寸 import (
    fun_计算单个文字的尺寸,
)
from MaterialEdit.type import _COLOR, _FONT_WEIGHT


def fun_单行文字转图片2(
    text: str,
    size: int,
    fill: _COLOR,
    background: _COLOR,
    font_weight: _FONT_WEIGHT,
):
    """构建字体对象"""
    chinese_font_obj = ImageFont.truetype(
        font=fun_获取字体(font_name="noto", font_weight=font_weight),  # type: ignore
        size=size,
    )
    english_font_obj = ImageFont.truetype(
        font=fun_获取字体(font_name="sam", font_weight=font_weight),  # type: ignore
        size=int(size * 1.1),
    )

    """
    构建尺寸列表
    """
    size_list = []
    for t in text:
        if fun_是英文(t) is True:
            size_list.append(fun_计算单个文字的尺寸(text=t, true_font=english_font_obj))
        else:
            size_list.append(fun_计算单个文字的尺寸(text=t, true_font=chinese_font_obj))

    """
    计算背景图片的尺寸
    """
    background_image_size = fun_计算一行文字的宽度和高度(font_size_list=size_list)

    """
    制作背景图片
    """
    background_image = Image.new(
        "RGBA",
        (background_image_size.width, background_image_size.height),
        background,
    )

    """
    开始写字
    """
    draw = ImageDraw.Draw(background_image)
    left, top = 0, 0
    for t in text:
        if fun_是英文(t) is True:
            curr_font_size = fun_计算单个文字的尺寸(text=t, true_font=english_font_obj)
            top = 0 - int(curr_font_size.height * 0.15)
            draw.text((left, top), text=t, fill=fill, font=english_font_obj)
            left += curr_font_size.width

        else:
            top = 0
            draw.text((left, top), text=t, fill=fill, font=chinese_font_obj)
            left += fun_计算单个文字的尺寸(text=t, true_font=chinese_font_obj).width

    background_image = fun_删除图片边框(background_image)

    return background_image
