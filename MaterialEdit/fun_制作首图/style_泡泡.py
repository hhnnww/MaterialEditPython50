from PIL import Image

from MaterialEdit.fun_图片编辑.fun_单行文字转图片.fun_单行文字转图片2 import (
    fun_单行文字转图片2,
)
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片水印.fun_获取单个水印 import fun_获取单个水印
from MaterialEdit.fun_图片编辑.fun_画一个圆形横框 import fun_画一个圆形横框
from MaterialEdit.fun_图片编辑.fun_画一个圆角矩形 import fun_画一个圆角矩形


def style_paopao(im: Image.Image, title: str, material_format: str, material_id: str):
    # 黑色底部背景
    circle = fun_画一个圆角矩形(1500, 600, 80, (0, 0, 0, 255), (255, 255, 255, 255))
    circle = circle.crop((0, 300, circle.width, circle.height))
    style_im = Image.new("RGBA", (1500, 300), (0, 0, 0, 255))
    style_im.paste(circle, (0, 0), circle)

    ad_font_weight = "bold"
    # 加入会员全店免费
    huiyuan_ad_im = fun_单行文字转图片2(
        text="# 9.9元加入会员，全店免费",
        font_weight=ad_font_weight,
        size=30,
        fill=(255, 255, 255, 255),
        background=(0, 0, 0, 255),
    )

    # 素材广告语
    ad_im = fun_单行文字转图片2(
        text="泡泡素材 Paopaosucai.taobao.com",
        font_weight=ad_font_weight,
        size=30,
        fill=(255, 255, 255, 255),
        background=(0, 0, 0, 255),
    )

    # 左上角图片合并
    left_im = fun_图片横向拼接(
        image_list=[
            huiyuan_ad_im,
            fun_图片横向拼接(
                [fun_获取单个水印(40, (255, 255, 255, 255)), ad_im],
                10,
                align_item="end",
                background_color=(0, 0, 0, 255),
            ),
        ],
        spacing=30,
        align_item="end",
        background_color=(0, 0, 0, 255),
    )

    style_im.paste(left_im, (75, 45), left_im)

    # 素材格式
    if material_format.lower() == "psd":
        material_format = "ps"

    format_im = fun_单行文字转图片2(
        text=material_format.title(),
        font_weight="bold",
        size=60,
        fill=(255, 255, 255, 255),
        background=(0, 0, 0, 255),
    )

    style_im.paste(format_im, (1385, 40), format_im)

    # 素材数量和素材标题
    title_im = fun_单行文字转图片2(
        text=title,
        font_weight="bold",
        size=100,
        fill=(255, 255, 255, 255),
        background=(0, 0, 0, 255),
    )

    style_im.paste(title_im, (65, 140), title_im)

    bg = fun_图片竖向拼接(
        [im, style_im],
        spacing=0,
        align_item="center",
        background_color=(255, 255, 255, 255),
    )

    material_id_pil = fun_单行文字转图片2(
        text="ID:" + material_id,
        font_weight="heavy",
        size=25,
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

    bg.paste(material_id_bg, (30, 30), material_id_bg)

    return bg
