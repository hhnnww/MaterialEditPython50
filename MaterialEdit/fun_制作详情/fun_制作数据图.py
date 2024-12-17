from MaterialEdit.fun_图片编辑.fun_ibm_font.fun_ibm_font import MakeIbmFont
from MaterialEdit.fun_图片编辑.fun_图片切换到圆角 import fun_图片切换到圆角
from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片画边框 import fun_图片画边框
from MaterialEdit.fun_图片编辑.fun_多行文字转图片.fun_文字换行 import fun_文字换行
from MaterialEdit.setting import FONT_COLOR
from MaterialEdit.type import _COLOR


def _fun_制作单行数据图(title: str, desc: str, background_color: _COLOR):
    font_weight = "light"
    # 制作key图片
    title_pil = MakeIbmFont(
        text=title,
        size=45,
        weight=font_weight,
        color=FONT_COLOR,
        bg_color=background_color,
    ).main()
    # 制作value图片
    text_split = fun_文字换行(text=desc, line_max_number=20)
    text_pil_list = []
    for t in text_split:
        obj = MakeIbmFont(
            text=t,
            color=FONT_COLOR,
            size=45,
            bg_color=background_color,
            weight=font_weight,
        )
        text_pil_list.append(obj.main())

    desc_pil = fun_图片竖向拼接(
        image_list=text_pil_list,
        spacing=20,
        align_item="start",
        background_color=background_color,
    )

    in_spacing = 180 - title_pil.width

    im = fun_图片横向拼接(
        image_list=[title_pil, desc_pil],
        background_color=background_color,
        spacing=150 + in_spacing,
        align_item="start",
    )

    im = fun_图片扩大粘贴(
        im, im.width + 180, im.height + 150, "center", "center", background_color
    )
    im = fun_图片扩大粘贴(im, 1420, im.height, "start", "center", background_color)

    return im


def fun_制作数据图(data_text: list[tuple[str, str]]):
    image_list = []
    for num, data_line_text in enumerate(data_text):
        if num % 2 == 0:
            background_color = (255, 255, 255, 255)
        else:
            background_color = (250, 250, 250, 255)
        image_list.append(
            _fun_制作单行数据图(
                title=data_line_text[0],
                desc=data_line_text[1],
                background_color=background_color,
            )
        )

    im = fun_图片竖向拼接(image_list, 0, "start", (255, 255, 255, 255))
    im = fun_图片画边框(im, (240, 240, 240, 255))
    im = fun_图片切换到圆角(im, 20)

    return im
