"""给图片添加蜘蛛水印。"""

from pathlib import Path

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_ibm_font.fun_ibm_font import MakeIbmFont
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.fun_图片编辑.fun_图片水印.fun_获取单个水印 import fun_获取单个水印


def __fun_制作单个水印(shop_name: str) -> Image.Image:
    """制作单个蜘蛛水印。"""
    shop_name_pil = MakeIbmFont(
        text=f"{shop_name}",
        size=120,
        color=(0, 0, 0, 255),
        bg_color=(0, 0, 0, 0),
        weight="semibold",
    ).main()
    logo = fun_图片竖向拼接(
        image_list=[
            fun_获取单个水印(size=480, fill_clor=(0, 0, 0, 255)),
            shop_name_pil,
        ],
        spacing=60,
        align_item="center",
        background_color=(0, 0, 0, 0),
    )

    # 修改颜色为180,180,180透明度
    for x in range(logo.width):
        for y in range(logo.height):
            r, g, b, a = logo.getpixel((x, y))
            logo.putpixel((x, y), (125, 125, 125, int(a * 0.5)))

    line_bg = Image.open(Path(__file__).parent / "line.png")
    line_bg.paste(
        im=logo,
        box=((line_bg.width - logo.width) // 2, (line_bg.height - logo.height) // 2),
        mask=logo,
    )

    return line_bg


def fun_蜘蛛水印2(im: Image.Image, shop_name: str) -> Image.Image:
    """给图片添加蜘蛛水印。"""
    zhizhu = __fun_制作单个水印(shop_name)
    zhizhu_width = im.width // 4
    zhizhu.thumbnail((zhizhu_width, 999999), Image.Resampling.LANCZOS)

    x, y = 0, 0
    while x < im.width:
        while y < im.height:
            im.paste(zhizhu, (x, y), mask=zhizhu)
            y += zhizhu.height
        x += zhizhu.width
        y = 0
    return im


if __name__ == "__main__":
    im = Image.open(r"C:\Users\aimlo\Desktop\UPLOAD\xq_1.jpg")
    bg = fun_蜘蛛水印2(im, "淘宝:小夕素材")
    bg.show()
