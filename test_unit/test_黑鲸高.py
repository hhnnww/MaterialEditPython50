from PIL import Image

from MaterialEdit.fun_制作首图.style_黑鲸高 import style_黑鲸高

im = Image.new("RGBA", (1500, 1250))
bg = style_黑鲸高(
    im=im,
    title="78套 国潮海报插画",
    format="psd",
    material_id="H0987",
    shop_name="泡泡素材",
)
bg.show()
