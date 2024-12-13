from PIL import Image

from .fun_单点删除边框 import DelPILBorder


def fun_删除图片边框(im: Image.Image) -> Image.Image:
    pix_list = [
        im.getpixel((0, 0)),
        im.getpixel((im.width - 1, 0)),
        im.getpixel((0, im.height - 1)),
        im.getpixel((im.width - 1, im.height - 1)),
    ]

    pix_list = list(set(pix_list))

    for pix_color in pix_list:
        im = DelPILBorder(img=im, border_color=pix_color).main()

    return im
