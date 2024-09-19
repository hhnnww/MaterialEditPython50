from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片切换到圆角 import fun_图片切换到圆角
from MaterialEdit.fun_图片编辑.fun_图片画边框 import fun_图片画边框
from MaterialEdit.setting import FIRST_IMAGE_BORDER_COLOR, FIRST_IMAGE_RATIO


def fun_图片边框圆角(im: Image.Image) -> Image.Image:
    im = fun_图片画边框(im, border_color=FIRST_IMAGE_BORDER_COLOR)
    im = fun_图片切换到圆角(im, FIRST_IMAGE_RATIO, (255, 255, 255, 255))

    return im
