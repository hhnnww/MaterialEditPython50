from PIL import Image

from MaterialEdit.fun_图片编辑.fun_ibm_font.fun_ibm_font import MakeIbmFont
from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_画一个圆形横框 import fun_画一个圆形横框


def fun_制作详情栏目标题(title: str, desc: str) -> Image.Image:
    """制作栏目大标题的图片

    Returns:
        _type_: _description_
    """
    font_color = (60, 60, 90, 255)
    title_pil = MakeIbmFont(
        weight="bold", text=title, size=60, bg_color=(0, 0, 0, 0), color=font_color
    ).main()
    circle = fun_画一个圆形横框(
        width=title_pil.width + 20,
        height=20,
        fill_color=(255, 230, 185, 255),
        background_color=(255, 255, 255, 0),
    )
    im1 = Image.new(
        mode="RGBA",
        size=(max([title_pil.width, circle.width]), title_pil.height + circle.height),
        color=(255, 255, 255, 255),
    )
    im1.paste(
        im=circle,
        box=(int((im1.width - circle.width) / 2), im1.height - circle.height),
        mask=circle,
    )
    im1.paste(
        im=title_pil, box=(int((im1.width - title_pil.width) / 2), 10), mask=title_pil
    )
    desc_pil = MakeIbmFont(
        text=desc,
        weight="text",
        size=30,
        color=font_color,
        bg_color=(255, 255, 255, 0),
    ).main()

    im = fun_图片竖向拼接(
        image_list=[im1, desc_pil],
        spacing=25,
        align_item="center",
        background_color=(255, 255, 255, 0),
    )
    im = fun_图片扩大粘贴(
        im=im,
        width=1500,
        height=im.height + 200,
        left="center",
        top="center",
        background_color=(255, 255, 255, 255),
    )
    im = fun_图片扩大粘贴(
        im=im,
        width=1500,
        height=im.height + 200,
        left="center",
        top="end",
        background_color=(255, 255, 255, 255),
    )
    return im
