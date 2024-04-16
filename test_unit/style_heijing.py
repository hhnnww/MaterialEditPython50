from PIL import Image

from MaterialEdit.fun_制作首图.style_黑鲸 import style_heijing

im = Image.new("RGBA", (1500, 1300), (255, 255, 255, 255))
style_heijing(im=im, title="238套 重阳节海报", material_format="PPTX", material_id="7898").show()
