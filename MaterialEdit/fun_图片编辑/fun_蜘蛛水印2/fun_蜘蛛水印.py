"""给图片添加蜘蛛水印。"""

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_ibm_font.fun_ibm_font import MakeIbmFont
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片水印.fun_获取单个水印 import fun_获取单个水印


def __fun_制作单个水印(shop_name: str) -> Image.Image:
    """制作单个蜘蛛水印。"""
    line_num = 4
    fill_color = (120, 120, 120, 60)
    shop_name_pil = MakeIbmFont(
        text=f"{shop_name}",
        size=120,
        color=fill_color,
        bg_color=(0, 0, 0, 0),
        weight="semibold",
    ).main()

    logo = fun_图片竖向拼接(
        image_list=[
            fun_获取单个水印(size=400, fill_clor=fill_color),
            shop_name_pil,
        ],
        spacing=60,
        align_item="center",
        background_color=(0, 0, 0, 0),
    )

    line_bg = Image.new("RGBA", (2000, 2000), (255, 255, 255, 0))

    line_bg.paste(
        logo,
        ((line_bg.width - logo.width) // 2, (line_bg.height - logo.height) // 2),
    )

    bg = Image.new(
        "RGBA",
        (line_bg.width * line_num, line_bg.height + logo.height),
        (255, 255, 255, 0),
    )
    left, top = 0, 0
    for _x in range(line_num):
        bg.paste(line_bg, (left, top))
        left += line_bg.width

    return bg


def fun_蜘蛛水印2(im: Image.Image, shop_name: str) -> Image.Image:
    """给图片添加蜘蛛水印。"""
    zhizhu = __fun_制作单个水印(shop_name)
    zhizhu.thumbnail((im.width, 999999), Image.Resampling.LANCZOS)

    im.paste(zhizhu, (0, int((im.height - zhizhu.height) / 2)), zhizhu)
    return im


if __name__ == "__main__":
    logo = __fun_制作单个水印(shop_name="小夕素材")
    bg = Image.new("RGBA", logo.size, (255, 255, 255, 255))
    bg.paste(logo, (0, 0), logo)
    bg.show()
