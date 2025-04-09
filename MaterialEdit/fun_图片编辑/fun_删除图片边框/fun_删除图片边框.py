from PIL import Image

from MaterialEdit.fun_图片编辑.fun_删除图片边框.fun_单点删除边框 import DelPILBorder


def fun_删除图片边框(im: Image.Image) -> Image.Image:
    """删除图片透明边框"""
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
