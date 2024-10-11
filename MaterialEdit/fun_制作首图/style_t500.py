from PIL import Image
from pypinyin import lazy_pinyin

from MaterialEdit.fun_图片编辑.fun_单行文字转图片.fun_单行文字转图片 import (
    fun_单行文字转图片,
)
from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_画一个圆形横框 import fun_画一个圆形横框
from MaterialEdit.fun_图片编辑.fun_画一个圆角矩形 import fun_画一个圆角矩形

from ..fun_图片编辑.fun_图片水印.fun_获取单个水印 import fun_获取单个水印


def fun_T500首图(
    im: Image.Image, title: str, format_title: str, shop_name: str, material_id: str
):
    circle = fun_画一个圆角矩形(
        width=550,
        height=550,
        border_radius=999,
        fill_color=(0, 0, 0, 255),
        background_color=(255, 255, 255, 0),
    )
    water_pil = fun_获取单个水印(100, (255, 200, 85, 255))
    water_pil_shop_name = fun_单行文字转图片(
        text=shop_name,
        chinese_font_name="noto",
        english_font_name="montserrat",
        font_weight="heavy",
        font_size=18,
        fill_color=(255, 200, 85, 255),
        background_color=(0, 0, 0, 255),
    )
    water_pil_shop_english = fun_单行文字转图片(
        text="".join(lazy_pinyin(shop_name)),
        chinese_font_name="zihun",
        english_font_name="montserrat",
        font_weight="heavy",
        font_size=12,
        fill_color=(255, 200, 85, 255),
        background_color=(0, 0, 0, 255),
    )
    water_pil_shop_name = fun_图片竖向拼接(
        [water_pil_shop_name, water_pil_shop_english], 5, "center", (0, 0, 0, 255)
    )
    water_pil = fun_图片竖向拼接(
        [water_pil, water_pil_shop_name], 10, "center", (0, 0, 0, 255)
    )
    circle.paste(
        water_pil,
        (
            int((circle.width - water_pil.width) / 2),
            int((((circle.height - 250) / 2) - water_pil.height) / 2),
        ),
        water_pil,
    )
    # 圆形的下面
    ad_2_pil = fun_单行文字转图片(
        text=shop_name + " 只卖精品",
        chinese_font_name="opposans",
        english_font_name="montserrat",
        font_weight="bold",
        font_size=30,
        fill_color=(255, 200, 85, 255),
        background_color=(0, 0, 0, 255),
    )
    material_id_pil = fun_单行文字转图片(
        text="ID: " + material_id,
        chinese_font_name="opposans",
        english_font_name="montserrat",
        font_weight="bold",
        font_size=28,
        fill_color=(255, 200, 85, 255),
        background_color=(0, 0, 0, 255),
        en_size_expand_ratio=1,
    )
    bottom_pil = fun_图片竖向拼接(
        [ad_2_pil, material_id_pil], 20, "center", (0, 0, 0, 255)
    )
    circle.paste(
        bottom_pil,
        (
            int((circle.width - bottom_pil.width) / 2),
            int((((circle.height - 250) / 2) - bottom_pil.height) / 2)
            + int(((circle.height - 250) / 2) + 250)
            - 10,
        ),
        bottom_pil,
    )
    im = fun_图片扩大粘贴(
        im=circle,
        width=im.width,
        height=im.height,
        left="center",
        top="center",
        background_color=(255, 255, 255, 0),
        background_pil=im,
    )

    # 画横框 写标题
    big_circle = fun_画一个圆形横框(
        width=950,
        height=250,
        fill_color=(255, 200, 85, 255),
        background_color=(255, 255, 255, 0),
    )
    title_pil = fun_单行文字转图片(
        text=title,
        chinese_font_name="misans",
        english_font_name="montserrat",
        font_weight="heavy",
        font_size=100,
        fill_color=(0, 0, 0, 255),
        background_color=(255, 200, 85, 255),
    )
    title_pil.thumbnail((790, 170), resample=Image.Resampling.LANCZOS, reducing_gap=3)
    big_circle.paste(
        title_pil,
        (
            int((big_circle.width - title_pil.width) / 2),
            int((190 - title_pil.height) / 2),
        ),
        title_pil,
    )

    # 写格式
    format_circle_pil = fun_画一个圆形横框(320, 55, (0, 0, 0, 255), (255, 200, 85, 255))
    format_title_pil = fun_单行文字转图片(
        text=format_title,
        chinese_font_name="opposans",
        english_font_name="montserrat",
        font_weight="heavy",
        font_size=30,
        fill_color=(255, 200, 85, 255),
        background_color=(0, 0, 0, 255),
        en_size_expand_ratio=1,
    )
    format_title_pil.thumbnail(
        (format_circle_pil.width, format_circle_pil.height), Image.Resampling.LANCZOS, 3
    )
    format_circle_pil.paste(
        format_title_pil,
        (
            int((format_circle_pil.width - format_title_pil.width) / 2),
            int((format_circle_pil.height - format_title_pil.height) / 2),
        ),
        format_title_pil,
    )
    big_circle.paste(format_circle_pil, (80, 170), format_circle_pil)

    # 写广告语
    ad_title_pil = fun_单行文字转图片(
        "全元素可编辑 全自动秒发货",
        chinese_font_name="opposans",
        english_font_name="montserrat",
        font_weight="bold",
        font_size=35,
        fill_color=(0, 0, 0, 255),
        background_color=(255, 200, 85, 255),
        en_size_expand_ratio=1,
    )
    big_circle.paste(
        ad_title_pil, (80 + format_circle_pil.width + 30, 180), ad_title_pil
    )

    im = fun_图片扩大粘贴(
        im=big_circle,
        width=im.width,
        height=im.height,
        left="center",
        top="center",
        background_color=(255, 255, 255, 0),
        background_pil=im,
    )

    return im
