from PIL import Image

from MaterialEdit.fun_图片编辑 import ImageEdit

im = Image.open(r"F:\小夕素材\5000-5999\5806\预览图\100_199\小夕素材(111).png")
im.thumbnail((800, 800), Image.LANCZOS, 3)
im = ImageEdit.fun_图片切换到圆角(im, 20, (255, 255, 255, 255))
im = ImageEdit.fun_图片扩大粘贴(im, im.width + 60, im.height + 60, "center", "center", (255, 255, 255, 255))
im.show()
