from pathlib import Path

from MaterialEdit.fun_制作首图.layout_小元素排列 import Layout小元素排列
from MaterialEdit.type import ImageModel

img_list = []
for in_file in Path(r"F:\小夕素材\10000-20000\10715\效果图").iterdir():
    if in_file.is_file() and in_file.suffix.lower() == ".png":
        img_list.append(ImageModel(path=in_file.as_posix()))

ly = Layout小元素排列(
    image_list=img_list,
    xq_width=1500,
    xq_height=1300,
    spacing=10,
    col=5,
    crop_position="center",
).main()


print(ly.size)
ly.show()
