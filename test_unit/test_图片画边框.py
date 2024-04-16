from MaterialEdit.fun_图片编辑 import ImageEdit
from PIL import Image


im = Image.open(r"F:\小夕素材\5000-5999\5806\预览图\100_199\小夕素材(111).png")
im.thumbnail((800, 800), Image.LANCZOS, 3)

im = ImageEdit.fun_图片画边框(im, (255, 255, 255, 255))
im = ImageEdit.fun_图片切换到圆角(im, 10)
im.show()
