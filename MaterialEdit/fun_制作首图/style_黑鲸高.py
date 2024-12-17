"""制作黑鲸首图"""

from PIL import Image

from MaterialEdit.fun_制作首图.fun_制作格式 import fun_制作格式
from MaterialEdit.fun_图片编辑.fun_ibm_font.fun_ibm_font import MakeIbmFont
from MaterialEdit.fun_图片编辑.fun_单行文字转图片.fun_单行文字转图片 import (
    fun_单行文字转图片,
)
from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片水印.fun_获取单个水印 import fun_获取单个水印
from MaterialEdit.fun_图片编辑.fun_画一个圆角矩形 import fun_画一个圆角矩形


def style_黑鲸高(
    im: Image.Image, title: str, format: str, material_id: str, shop_name: str
) -> Image.Image:
    """制作黑鲸首图

    Returns:
        _type_: _description_
    """
    if im.width < 1500 or im.height < 1250:
        im = fun_图片扩大粘贴(im, 1500, 1250, "center", "center", (255, 255, 255, 255))

    # title_pil = fun_单行文字转图片(
    #     text=title,
    #     font_weight="bold",
    #     font_size=85,
    #     fill_color=(255, 255, 255, 255),
    #     background_color=(0, 0, 0, 255),
    #     english_font_name="montserrat",
    #     chinese_font_name="opposans",
    # )

    title_pil = MakeIbmFont(
        text=title,
        size=85,
        weight="bold",
        color=(255, 255, 255, 255),
        bg_color=(0, 0, 0, 255),
    ).main()

    # title_pil = fun_单行文字转图片2(
    #     text=title,
    #     size=80,
    #     fill=(255, 255, 255, 255),
    #     background=(255, 255, 255, 0),
    #     font_weight="bold",
    # )

    ad_pil = fun_单行文字转图片(
        text=f"{shop_name} - 9.9元加入会员，全店免费 Paopaosucai.taobao.com",
        font_weight="bold",
        font_size=25,
        fill_color=(255, 255, 255, 255),
        background_color=(0, 0, 0, 255),
        english_font_name="montserrat",
        chinese_font_name="opposans",
    )

    # ad_pil = fun_单行文字转图片2(
    #     text=f"{shop_name} - 9.9元加入会员，全店免费 Paopaosucai.taobao.com",
    #     size=30,
    #     fill=(255, 255, 255, 255),
    #     background=(0, 0, 0, 255),
    #     font_weight="normal",
    # )

    title_ad = fun_图片竖向拼接(
        image_list=[title_pil, ad_pil],
        spacing=25,
        align_item="start",
        background_color=(255, 255, 255, 0),
    )

    circle = fun_画一个圆角矩形(1500, 500, 80, (0, 0, 0, 255), (255, 255, 255, 255))
    circle = circle.crop((0, 250, circle.width, circle.height))
    circle.paste(title_ad, (80, int((circle.height - title_ad.height) / 2)), title_ad)

    bg = fun_图片竖向拼接(
        image_list=[im, circle],
        spacing=0,
        align_item="center",
        background_color=(255, 255, 255, 255),
    )

    format_im = fun_制作格式(material_format=format)

    left = 1500 - format_im.width - 80
    top = int(1500 - circle.height - (format_im.height / 2))
    bg.paste(format_im, (left, top), format_im)

    # LOGO
    water_pil = fun_获取单个水印(60, fill_clor=(255, 255, 255, 255))
    water_pil_bg = fun_画一个圆角矩形(
        width=water_pil.width + 50,
        height=int(water_pil.height * 2) + 90,
        border_radius=80,
        background_color=(255, 255, 255, 0),
        fill_color=(0, 0, 0, 255),
    )
    water_pil_bg = water_pil_bg.crop(
        (0, int(water_pil_bg.height / 2), water_pil_bg.width, water_pil_bg.height)
    )

    water_pil_bg.paste(
        water_pil,
        (
            int((water_pil_bg.width - water_pil.width) / 2),
            int((water_pil_bg.height - water_pil.height) / 2) - 5,
        ),
        water_pil,
    )
    bg.paste(water_pil_bg, (55, 0), water_pil_bg)

    id_pil = fun_单行文字转图片(
        text=f"ID:{material_id}",
        font_size=20,
        fill_color=(255, 255, 255, 255),
        font_weight="heavy",
        english_font_name="montserrat",
        chinese_font_name="noto",
        background_color=(0, 0, 0, 255),
    )

    id_bg = fun_画一个圆角矩形(
        width=id_pil.width + 50,
        height=id_pil.height + 30,
        border_radius=30,
        fill_color=(0, 0, 0, 255),
        background_color=(0, 0, 0, 0),
    )

    id_bg.paste(
        id_pil,
        (
            int((id_bg.width - id_pil.width) / 2),
            int((id_bg.height - id_pil.height) / 2),
        ),
        id_pil,
    )

    bg.paste(id_bg, (bg.width - id_bg.width - 30, 30), id_bg)

    return bg
