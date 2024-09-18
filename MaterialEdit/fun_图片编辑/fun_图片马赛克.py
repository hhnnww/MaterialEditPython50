from PIL import Image


def fun_图片马赛克(im: Image.Image):
    size = im.size
    im.thumbnail((int(im.width / 30), int(im.height / 30)))
    im = im.resize(size)
    return im
