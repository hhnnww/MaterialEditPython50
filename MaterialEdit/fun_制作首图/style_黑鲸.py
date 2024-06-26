from PIL import Image

from ..fun_图片编辑 import ImageEdit


def fun_黑鲸首图(
    im: Image.Image, title: str, material_format: str, material_id: str
) -> Image.Image:
    # 制作素材ID
    material_id_pil = ImageEdit.fun_单行文字转图片(
        text="ID:" + material_id,
        chinese_font_name="opposans",
        english_font_name="montserrat",
        font_weight="heavy",
        font_size=20,
        fill_color=(255, 255, 255, 255),
        background_color=(0, 0, 0, 255),
        en_size_expand_ratio=1,
    )
    material_id_bg = ImageEdit.fun_画一个圆形横框(
        material_id_pil.width + 40,
        material_id_pil.height + 20,
        (0, 0, 0, 255),
        (255, 255, 255, 0),
    )
    material_id_bg.paste(material_id_pil, (20, 10), material_id_pil)
    im.paste(material_id_bg, (30, 30), material_id_bg)

    # 画边框和写标题
    circle = ImageEdit.fun_画一个圆角矩形(
        1500, 400, 80, (0, 0, 0, 255), (255, 255, 255, 255)
    )
    circle = circle.crop((0, 200, circle.width, circle.height))
    title_pil = ImageEdit.fun_单行文字转图片(
        text=title,
        chinese_font_name="opposans",
        english_font_name="montserrat",
        font_weight="bold",
        font_size=85,
        fill_color=(255, 255, 255, 255),
        background_color=(0, 0, 0, 255),
        en_size_expand_ratio=1,
    )
    circle.paste(
        title_pil, (80, int((circle.height - title_pil.height) / 2)), title_pil
    )

    bg = ImageEdit.fun_图片竖向拼接([im, circle], 0, "center", (255, 255, 255, 255))

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
    format_bg_circle = ImageEdit.fun_画一个圆(
        195, 195, fill_color=background_color, background_color=(255, 255, 255, 0)
    )
    format_fill_circle = ImageEdit.fun_画一个圆(
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

    format_pil = ImageEdit.fun_单行文字转图片(
        text=material_format.upper(),
        chinese_font_name="opposans",
        english_font_name="montserrat",
        font_weight="heavy",
        font_size=60,
        fill_color=text_color,
        background_color=fill_color,
    )
    format_pil.thumbnail(
        (int(format_bg_circle.width * 0.6), int(format_bg_circle.height * 0.6)),
        Image.LANCZOS,
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

    bg.paste(
        format_bg_circle,
        (
            int((bg.width - format_bg_circle.width) - 100),
            int(im.height - (format_bg_circle.height / 2)),
        ),
        format_bg_circle,
    )

    return bg
