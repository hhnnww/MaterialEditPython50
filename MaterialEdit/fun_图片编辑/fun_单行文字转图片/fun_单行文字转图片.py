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
from MaterialEdit.type import _COLOR, _FONT_NAME, _FONT_WEIGHT


def fun_单行文字转图片(
    text: str,
    chinese_font_name: _FONT_NAME,
    english_font_name: _FONT_NAME,
    font_weight: _FONT_WEIGHT,
    font_size: int,
    fill_color: _COLOR,
    background_color: _COLOR,
    en_size_expand_ratio: float = 1.2,
):
    en_size = int(font_size * en_size_expand_ratio)
    """
    构建字体对象
    """
    chinese_font_obj = ImageFont.truetype(
        font=fun_获取字体(font_name=chinese_font_name, font_weight=font_weight),
        size=font_size,
    )
    english_font_obj = ImageFont.truetype(
        font=fun_获取字体(font_name=english_font_name, font_weight=font_weight),
        size=en_size,
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
        background_color,
    )

    """
    开始写字
    """
    draw = ImageDraw.Draw(im=background_image)
    left, top = 0, 0
    for t in text:
        if fun_是英文(text=t) is True:
            curr_font_size = fun_计算单个文字的尺寸(text=t, true_font=english_font_obj)
            top = 0 - int(curr_font_size.height * ((en_size_expand_ratio - 1) / 2))
            draw.text(xy=(left, top), text=t, fill=fill_color, font=english_font_obj)
            left += curr_font_size.width

        else:
            top = 0
            draw.text(xy=(left, top), text=t, fill=fill_color, font=chinese_font_obj)
            left += fun_计算单个文字的尺寸(text=t, true_font=chinese_font_obj).width

    # background_image = DelPILBorder(
    #     img=background_image, border_color=None
    # ).main()

    background_image = fun_删除图片边框(background_image)

    return background_image
