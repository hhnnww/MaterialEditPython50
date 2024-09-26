from pathlib import Path

from MaterialEdit.fun_制作首图.layout_1大竖_2排小竖 import Layout1大竖2排小竖
from MaterialEdit.type import ImageModel

ma_path = Path(r"D:\泡泡素材\0000-0999\0726\预览图")

pic_list = []
for in_file in ma_path.iterdir():
    if (
        in_file.is_file()
        and "thumb" not in in_file.stem
        and in_file.suffix.lower() in [".png"]
    ):
        pic_list.append(ImageModel(path=in_file.as_posix()))

        if len(pic_list) > 8:
            break


bg = Layout1大竖2排小竖(
    image_list=pic_list,
    xq_width=1500,
    xq_height=1300,
    spacing=10,
    col=0,
    crop_position="center",
).main()
bg.show()
