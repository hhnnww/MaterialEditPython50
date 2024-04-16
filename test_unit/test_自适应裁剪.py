from pathlib import Path

from PIL import Image

from MaterialEdit import LayoutAdaptiveCrop
from MaterialEdit.type import ImageModel

image_list = []


for in_file in Path(r"F:\小夕素材\重阳节\预览图").iterdir():
    if in_file.is_file() and in_file.suffix.lower() in [".png"]:
        with Image.open(in_file.as_posix()) as im:
            image_list.append(ImageModel(path=in_file.as_posix(), ratio=im.width / im.height))

            if len(image_list) >= 40:
                break

LayoutAdaptiveCrop(
    image_list=image_list,
    xq_width=1500,
    xq_height=1500,
    line=4,
    crop_position="center",
    spacing=10,
).run_制作自适应布局图片().show()
