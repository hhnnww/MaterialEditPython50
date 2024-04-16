from PIL import Image, ImageFont, ImageDraw

from MaterialEdit.fun_图片编辑 import ImageEdit
from MaterialEdit.fun_图片编辑.fun_单行文字转图片.fun_获取字体 import fun_获取字体


def fun_制作详情栏目标题(title: str, desc: str) -> Image.Image:
    font_color = (60, 60, 90, 255)
    font_path = fun_获取字体(font_name="opposans", font_weight="bold")
    true_font = ImageFont.truetype(font=font_path, size=60)
    _l, _t, width, height = true_font.getbbox(text=title)

    circle = ImageEdit.fun_画一个圆形横框(
        width=width + 20,
        height=20,
        fill_color=(255, 230, 185),
        background_color=(255, 255, 255, 255),
    )

    im = Image.new("RGBA", (circle.width, circle.height + height - 10), (255, 255, 255, 255))
    im.paste(circle, (0, im.height - circle.height), circle)

    draw = ImageDraw.Draw(im)
    draw.text(xy=(10, 0), text=title, fill=font_color, font=true_font)

    desc_pil = ImageEdit.fun_单行文字转图片(
        text=desc,
        chinese_font_name="opposans",
        english_font_name="montserrat",
        font_weight="normal",
        font_size=30,
        fill_color=font_color,
        background_color=(255, 255, 255, 0),
        en_size_expand_ratio=1,
    )

    im = ImageEdit.fun_图片竖向拼接([im, desc_pil], 25, "center", (255, 255, 255, 0))
    im = ImageEdit.fun_图片扩大粘贴(
        im=im, width=1500, height=im.height + 200, left="center", top="center", background_color=(255, 255, 255, 255)
    )
    im = ImageEdit.fun_图片扩大粘贴(
        im=im, width=1500, height=im.height + 200, left="center", top="end", background_color=(255, 255, 255, 255)
    )
    return im
