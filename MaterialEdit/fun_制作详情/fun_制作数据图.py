from MaterialEdit.fun_图片编辑 import ImageEdit
from MaterialEdit.setting import FONT_COLOR
from MaterialEdit.type import _COLOR


def _fun_制作单行数据图(title: str, desc: str, background_color: _COLOR):
    title_pil = ImageEdit.fun_单行文字转图片(
        text=title,
        chinese_font_name="misans",
        english_font_name="montserrat",
        fill_color=FONT_COLOR,
        background_color=background_color,
        font_size=45,
        font_weight="normal",
        en_size_expand_ratio=1,
    )

    desc_pil = ImageEdit.fun_制作多行本文(
        text=desc,
        spacing=20,
        line_max_number=20,
        chinese_font_name="misans",
        english_font_name="montserrat",
        fill_color=FONT_COLOR,
        background_color=background_color,
        font_size=45,
        font_weight="normal",
        en_size_expand_ratio=1,
    )

    in_spacing = 180 - title_pil.width

    im = ImageEdit.fun_图片横向拼接(
        image_list=[title_pil, desc_pil],
        background_color=background_color,
        spacing=150 + in_spacing,
        align_item="start",
    )

    im = ImageEdit.fun_图片扩大粘贴(im, im.width + 180, im.height + 150, "center", "center", background_color)
    im = ImageEdit.fun_图片扩大粘贴(im, 1420, im.height, "left", "center", background_color)
    return im


def fun_制作数据图(data_text: list[tuple[str, str]]):
    image_list = []
    for num, data_line_text in enumerate(data_text):
        if num % 2 == 0:
            background_color = (255, 255, 255, 255)
        else:
            background_color = (250, 250, 250, 255)
        image_list.append(
            _fun_制作单行数据图(title=data_line_text[0], desc=data_line_text[1], background_color=background_color)
        )

    im = ImageEdit.fun_图片竖向拼接(image_list, 0, "start", (255, 255, 255, 255))
    im = ImageEdit.fun_图片画边框(im, (240, 240, 240, 255))
    im = ImageEdit.fun_图片切换到圆角(im, 20)
    return im
