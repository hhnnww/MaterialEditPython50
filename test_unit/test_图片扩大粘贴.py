from PIL import Image

from MaterialEdit.fun_图片编辑 import ImageEdit

im = Image.new("RGBA", (300, 300), (255, 255, 255, 255))
im = ImageEdit.fun_图片扩大粘贴(im, 400, 400, "center", "center", (0, 0, 0, 255))
im.show()
