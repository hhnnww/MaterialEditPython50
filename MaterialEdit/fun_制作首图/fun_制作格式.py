from PIL import Image

from MaterialEdit.fun_图片编辑.fun_单行文字转图片.fun_单行文字转图片2 import (
    fun_单行文字转图片2,
)
from MaterialEdit.fun_图片编辑.fun_画一个圆形 import fun_画一个圆


def fun_制作格式(material_format: str):
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

    return format_bg_circle


if __name__ == "__main__":
    fun_制作格式(material_format="psd").show()
