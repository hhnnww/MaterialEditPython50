from PIL import Image

from MaterialEdit.fun_图片编辑.fun_单行文字转图片.fun_单行文字转图片 import (
    fun_单行文字转图片,
)
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片水印.fun_获取单个水印 import fun_获取单个水印

from ..setting import FONT_COLOR


def fun_小图增加信息(im: Image.Image, title: str, desc: str):
    water_pil = fun_获取单个水印(80, fill_clor=FONT_COLOR)

    title_pil = fun_单行文字转图片(
        text=title.upper(),
        chinese_font_name="opposans",
        english_font_name="montserrat",
        font_weight="normal",
        font_size=40,
        fill_color=FONT_COLOR,
        background_color=(255, 255, 255, 255),
        en_size_expand_ratio=1,
    )

    desc_pil = fun_单行文字转图片(
        text=desc.replace(".", "").upper(),
        chinese_font_name="opposans",
        english_font_name="montserrat",
        font_weight="normal",
        font_size=33,
        fill_color=FONT_COLOR,
        background_color=(255, 255, 255, 255),
        en_size_expand_ratio=1,
    )

    bg = fun_图片竖向拼接(
        [water_pil, title_pil, desc_pil],
        spacing=20,
        align_item="center",
        background_color=(255, 255, 255, 255),
    )

    bg.thumbnail(
        (int(im.width * 0.8), 999), resample=Image.Resampling.LANCZOS, reducing_gap=3
    )

    bg = fun_图片竖向拼接(
        [im, bg], spacing=50, align_item="center", background_color=(255, 255, 255, 255)
    )

    return bg
