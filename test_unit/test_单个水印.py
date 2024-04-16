# fun_获取单个水印(70, (0, 255, 255, 255)).show()
from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片水印.fun_图片打满水印 import fun_图片打满水印

im = Image.open(r"G:\饭桶设计\1000-1999\1990\预览图\饭桶设计(5).png").convert("RGBA")
im.thumbnail((1200, 1200))
pixel_color = int(255 * 0.6)
fun_图片打满水印(
    im=im, size=50, line_number=3, singe_line_number=1, water_color=(pixel_color, pixel_color, pixel_color, pixel_color)
).show()
