from PIL import Image


def fun_裁剪图片(im: Image.Image, max_singe_height: int = 2500):
    top, bottom = 0, max_singe_height

    while top < im.height:
        if bottom > im.height:
            bottom = im.height

        yield im.crop((0, top, im.width, bottom))

        top += max_singe_height
        bottom += max_singe_height
