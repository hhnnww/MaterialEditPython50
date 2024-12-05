from pathlib import Path

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_单行文字转图片.fun_单行文字转图片2 import (
    fun_单行文字转图片2,
)
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片水印.fun_获取单个水印 import fun_获取单个水印
from MaterialEdit.fun_图片编辑.fun_画一个圆形 import fun_画一个圆
from MaterialEdit.fun_图片编辑.fun_画一个圆形横框 import fun_画一个圆形横框
from MaterialEdit.fun_图片编辑.fun_画一个圆角矩形 import fun_画一个圆角矩形


def fun_黑鲸首图(
    im: Image.Image, title: str, material_format: str, material_id: str, shop_name: str
) -> Image.Image:
    if im.width > 1500:
        im = im.crop((0, 0, 1500, im.height))

    # 制作素材ID
    material_id_pil = fun_单行文字转图片2(
        text="ID:" + material_id,
        font_weight="heavy",
        size=20,
        fill=(255, 255, 255, 255),
        background=(0, 0, 0, 255),
    )

    material_id_bg = fun_画一个圆形横框(
        material_id_pil.width + 40,
        material_id_pil.height + 20,
        (0, 0, 0, 255),
        (255, 255, 255, 0),
    )

    material_id_bg.paste(material_id_pil, (20, 10), material_id_pil)
    im.paste(material_id_bg, (im.width - material_id_bg.width - 30, 30), material_id_bg)

    # 左边的logo
    logo = fun_获取单个水印(80, fill_clor=(255, 255, 255, 255))
    shop_name_pil = fun_单行文字转图片2(
        text=shop_name,
        size=40,
        fill=(255, 255, 255, 255),
        background=(0, 0, 0, 255),
        font_weight="heavy",
    )
    shop_name_pil.thumbnail(
        logo.size, resample=Image.Resampling.LANCZOS, reducing_gap=8
    )
    logo = fun_图片竖向拼接(
        [logo, shop_name_pil],
        spacing=10,
        align_item="center",
        background_color=(0, 0, 0, 255),
    )
    add_width = 60
    logo_bg = fun_画一个圆角矩形(
        width=logo.width + add_width,
        height=int((logo.height + 50) * 2),
        border_radius=50,
        fill_color=(0, 0, 0, 255),
    )
    logo_bg = logo_bg.crop((0, int(logo_bg.height / 2), logo_bg.width, logo_bg.height))
    logo_bg.paste(logo, (int(add_width / 2), 25), logo)

    im.paste(logo_bg, (60, 0), logo_bg)

    # 画边框和写标题
    circle = fun_画一个圆角矩形(1500, 400, 80, (0, 0, 0, 255), (255, 255, 255, 255))
    circle = circle.crop((0, 200, circle.width, circle.height))
    # circle = fun_画一个圆角矩形(1500, 200, 60, (0, 0, 0, 255), (255, 255, 255, 255))

    # title_pil = fun_单行文字转图片(
    #     text=title,
    #     font_weight="medium",
    #     font_size=100,
    #     fill_color=(255, 255, 255, 255),
    #     background_color=(0, 0, 0, 255),
    #     english_font_name="montserrat",
    #     chinese_font_name="noto",
    # )

    title_pil = fun_单行文字转图片2(
        text=title,
        size=100,
        fill=(255, 255, 255, 255),
        background=(0, 0, 0, 255),
        font_weight="medium",
    )

    circle.paste(
        title_pil, (80, int((circle.height - title_pil.height) / 2)), title_pil
    )

    bg = fun_图片竖向拼接([im, circle], 0, "center", (255, 255, 255, 255))

    # 格式圆圈背景
    if material_format.lower() in ["psd"]:
        background_color = (35, 200, 250, 255)
        fill_color = (5, 30, 35, 255)
        text_color = (35, 200, 250, 255)
    elif material_format.lower() in ["ppt", "pptx"]:
        background_color = (250, 135, 110, 255)
        fill_color = (185, 50, 25, 255)
        text_color = (255, 255, 255, 255)
    elif material_format.lower() in ["ai", "eps"]:
        background_color = (255, 155, 0, 255)
        fill_color = (50, 0, 0, 255)
        text_color = (255, 155, 0, 255)
    elif material_format.lower() in ["skp"]:
        background_color = (0, 99, 163, 255)
        fill_color = (12, 69, 115, 255)
        text_color = (255, 255, 255, 255)
    else:
        background_color = (250, 135, 110, 255)
        fill_color = (185, 50, 25, 255)
        text_color = (255, 255, 255, 255)

    # 制作格式
    format_bg_circle = fun_画一个圆(
        195, 195, fill_color=background_color, background_color=(255, 255, 255, 0)
    )
    format_fill_circle = fun_画一个圆(
        170, 170, fill_color=fill_color, background_color=(255, 255, 255, 0)
    )
    format_bg_circle.paste(
        format_fill_circle,
        (
            int((format_bg_circle.width - format_fill_circle.width) / 2),
            int((format_bg_circle.height - format_fill_circle.height) / 2),
        ),
        format_fill_circle,
    )

    format_title = material_format
    if format_title.lower() == "psd":
        format_title = "ps"

    # 格式文字
    format_pil = fun_单行文字转图片2(
        text=format_title.title(),
        font_weight="heavy",
        size=90,
        fill=text_color,
        background=fill_color,
    )
    format_pil.thumbnail(
        (int(format_bg_circle.width * 0.6), int(format_bg_circle.height * 0.6)),
        Image.Resampling.LANCZOS,
        3,
    )
    format_bg_circle.paste(
        format_pil,
        (
            int((format_bg_circle.width - format_pil.width) / 2),
            int((format_bg_circle.height - format_pil.height) / 2),
        ),
        format_pil,
    )

    # procreate 图标
    if material_format.lower() in ["pro", "procreate", "brushset", "abr"]:
        logo_path = Path(__file__).parent / "img" / "procreate.png"
        format_bg_circle = Image.open(logo_path)
        format_bg_circle.thumbnail((180, 180))

    elif material_format.lower() in ["cdr"]:
        logo_path = Path(__file__).parent / "img" / "cdr.png"
        format_bg_circle = Image.open(logo_path)
        format_bg_circle.thumbnail((180, 180))

    elif material_format.lower() in ["skp"]:
        logo_path = Path(__file__).parent / "img" / "su.png"
        format_bg_circle = Image.open(logo_path)
        format_bg_circle.thumbnail((180, 180))

    bg.paste(
        format_bg_circle,
        (
            int((bg.width - format_bg_circle.width) - 100),
            int(im.height - (format_bg_circle.height / 2)),
        ),
        format_bg_circle,
    )

    return bg
