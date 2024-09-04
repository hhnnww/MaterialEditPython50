from PIL import Image

from MaterialEdit.fun_图片编辑.fun_单行文字转图片.fun_单行文字转图片2 import (
    fun_单行文字转图片2,
)
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片水印.fun_获取单个水印 import fun_获取单个水印


def style_paopao(
    im: Image.Image, title: str, material_format: str, material_id: str, num: int
):
    style_im = Image.new("RGBA", (1500, 300), (0, 0, 0, 255))

    # 素材ID
    material_id_im = fun_单行文字转图片2(
        text=f"#{material_id}",
        font_weight="normal",
        size=30,
        fill=(255, 255, 255, 255),
        background=(0, 0, 0, 255),
    )

    # 素材广告语
    ad_im = fun_单行文字转图片2(
        text="泡泡素材 Paopaosucai.taobao.com",
        font_weight="normal",
        size=25,
        fill=(255, 255, 255, 255),
        background=(0, 0, 0, 255),
    )

    # 左上角图片合并
    left_im = fun_图片横向拼接(
        image_list=[
            material_id_im,
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
    num_title = f"{num}P"
    title_size = 90
    num_im = fun_单行文字转图片2(
        text=num_title.upper(),
        font_weight="bold",
        size=title_size,
        fill=(255, 255, 255, 255),
        background=(0, 0, 0, 255),
    )

    title_im = fun_单行文字转图片2(
        text=title,
        font_weight="bold",
        size=title_size,
        fill=(255, 255, 255, 255),
        background=(0, 0, 0, 255),
    )

    all_title_im = fun_图片横向拼接(
        image_list=[num_im, title_im],
        spacing=30,
        align_item="center",
        background_color=(0, 0, 0, 255),
    )

    style_im.paste(all_title_im, (65, 140), all_title_im)

    bg = fun_图片竖向拼接(
        [im, style_im],
        spacing=0,
        align_item="center",
        background_color=(255, 255, 255, 255),
    )
    return bg
