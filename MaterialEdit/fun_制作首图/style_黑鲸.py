"""制作黑鲸首图"""

from pathlib import Path

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_ibm_font.fun_ibm_font import MakeIbmFont
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片水印.fun_获取单个水印 import fun_获取单个水印
from MaterialEdit.fun_图片编辑.fun_画一个圆形 import fun_画一个圆
from MaterialEdit.fun_图片编辑.fun_画一个圆形横框 import fun_画一个圆形横框
from MaterialEdit.fun_图片编辑.fun_画一个圆角矩形 import fun_画一个圆角矩形


def fun_make_material_id_image(material_id: str) -> Image.Image:
    """制作右上角的素材ID."""
    # 制作素材ID
    material_id_pil = MakeIbmFont(
        text="ID:" + material_id,
        weight="bold",
        size=30,
        color=(255, 255, 255, 255),
        bg_color=(0, 0, 0, 255),
    ).main()

    material_id_bg = fun_画一个圆形横框(
        width=material_id_pil.width + 50,
        height=material_id_pil.height + 30,
        fill_color=(0, 0, 0, 255),
        background_color=(255, 255, 255, 0),
    )

    material_id_bg.paste(
        im=material_id_pil,
        box=(
            (material_id_bg.width - material_id_pil.width) // 2,
            ((material_id_bg.height - material_id_pil.height) // 2) - 2,
        ),
        mask=material_id_pil,
    )
    return material_id_bg


def fun_make_left_logo_image(shop_name: str) -> Image.Image:
    """制作左边的logo."""
    logo = fun_获取单个水印(size=120, fill_clor=(255, 255, 255, 255))
    shop_name_pil = MakeIbmFont(
        text=shop_name,
        size=50,
        color=(255, 255, 255, 255),
        bg_color=(0, 0, 0, 255),
        weight="bold",
    ).main()
    shop_name_pil.thumbnail(
        size=(logo.width + 20, 999999),
        resample=Image.Resampling.LANCZOS,
    )
    logo = fun_图片竖向拼接(
        image_list=[logo, shop_name_pil],
        spacing=20,
        align_item="center",
        background_color=(0, 0, 0, 255),
    )
    add_width = 60
    logo_bg = fun_画一个圆角矩形(
        width=logo.width + add_width,
        height=int((logo.height + 50) * 2),
        border_radius=35,
        fill_color=(0, 0, 0, 255),
    )
    logo_bg = logo_bg.crop(
        box=(0, int(logo_bg.height / 2), logo_bg.width, logo_bg.height),
    )
    logo_bg.paste(im=logo, box=(int(add_width / 2), 25), mask=logo)

    return logo_bg


def fun_make_title_image(title: str) -> Image.Image:
    """制作大标题."""
    circle = fun_画一个圆角矩形(
        width=1500,
        height=400,
        border_radius=80,
        fill_color=(0, 0, 0, 255),
        background_color=(255, 255, 255, 255),
    )
    circle = circle.crop(box=(0, 200, circle.width, circle.height))
    circle = circle.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    title_pil = MakeIbmFont(
        text=title,
        size=105,
        weight="text",
        color=(255, 255, 255, 255),
        bg_color=(0, 0, 0, 255),
    ).main()
    circle.paste(
        im=title_pil,
        box=(60, int((circle.height - title_pil.height) / 2)),
        mask=title_pil,
    )
    return circle


def fun_select_format_color(
    material_format: str,
) -> tuple[tuple[int, int, int, int], ...]:
    """制作格式图片."""
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

    return background_color, fill_color, text_color


def fun_make_format_image(material_format: str) -> Image.Image:
    """制作右下角格式的圆圈图片."""
    # 构建素材格式的颜色
    background_color, fill_color, text_color = fun_select_format_color(
        material_format=material_format,
    )

    # 制作格式
    format_bg_circle = fun_画一个圆(
        width=195,
        height=195,
        fill_color=background_color,
        background_color=(255, 255, 255, 0),
    )
    format_fill_circle = fun_画一个圆(
        width=170,
        height=170,
        fill_color=fill_color,
        background_color=(255, 255, 255, 0),
    )
    format_bg_circle.paste(
        im=format_fill_circle,
        box=(
            int((format_bg_circle.width - format_fill_circle.width) / 2),
            int((format_bg_circle.height - format_fill_circle.height) / 2),
        ),
        mask=format_fill_circle,
    )

    format_title = material_format
    if format_title.lower() == "psd":
        format_title = "ps"

    # 格式文字
    format_pil = MakeIbmFont(
        text=format_title.title(),
        weight="semibold",
        size=90,
        color=text_color,
        bg_color=fill_color,
    ).main()

    format_pil.thumbnail(
        size=(int(format_bg_circle.width * 0.6), int(format_bg_circle.height * 0.6)),
        resample=Image.Resampling.LANCZOS,
        reducing_gap=3,
    )

    format_bg_circle.paste(
        im=format_pil,
        box=(
            int((format_bg_circle.width - format_pil.width) / 2),
            int((format_bg_circle.height - format_pil.height) / 2),
        ),
        mask=format_pil,
    )

    # procreate 图标
    if material_format.lower() in ["pro", "procreate", "brushset", "abr"]:
        logo_path = Path(__file__).parent / "img" / "procreate.png"
        format_bg_circle = Image.open(fp=logo_path)
        format_bg_circle.thumbnail(size=(180, 180))

    # CDR图标
    elif material_format.lower() in ["cdr"]:
        logo_path = Path(__file__).parent / "img" / "cdr.png"
        format_bg_circle = Image.open(fp=logo_path)
        format_bg_circle.thumbnail(size=(180, 180))

    # SKP图标
    elif material_format.lower() in ["skp"]:
        logo_path = Path(__file__).parent / "img" / "su.png"
        format_bg_circle = Image.open(fp=logo_path)
        format_bg_circle.thumbnail(size=(180, 180))

    return format_bg_circle


def fun_黑鲸首图(
    im: Image.Image,
    title: str,
    material_format: str,
    material_id: str,
    shop_name: str,
    bg_color: tuple[int, ...],
) -> Image.Image:
    """制作黑鲸首图."""
    xq_width = 1500
    if im.width > xq_width:
        im = im.crop(box=(0, 0, 1500, im.height))

    bg = Image.new("RGBA", im.size, bg_color)
    bg.paste(im, (0, 0), im)
    im = bg

    # 制作素材ID
    material_id_bg = fun_make_material_id_image(material_id=material_id)
    im.paste(
        im=material_id_bg,
        box=(im.width - material_id_bg.width - 30, 30),
        mask=material_id_bg,
    )

    # 制作左边的LOGO
    logo_bg = fun_make_left_logo_image(shop_name=shop_name)
    im.paste(im=logo_bg, box=(60, 0), mask=logo_bg)

    # 画边框和写标题
    circle = fun_make_title_image(title=title)
    bg = fun_图片竖向拼接(
        image_list=[im, circle],
        spacing=0,
        align_item="center",
        background_color=(255, 255, 255, 255),
    )

    # 格式圆圈背景
    format_bg_circle = fun_make_format_image(material_format=material_format)

    bg.paste(
        im=format_bg_circle,
        box=(
            int((bg.width - format_bg_circle.width) - 100),
            int(im.height - (format_bg_circle.height / 2)),
        ),
        mask=format_bg_circle,
    )

    return bg
