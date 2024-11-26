from pathlib import Path

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接


def fun_享设计制作预览图(material_path: str, shop_name: str):
    for sub_path in Path(material_path).iterdir():
        if sub_path.is_dir():
            fun_制作文件夹大图(sub_path=sub_path, shop_name=shop_name)


def fun_制作文件夹大图(sub_path: Path, shop_name: str):
    png_file_list = []
    for in_file in sub_path.iterdir():
        if (
            in_file.is_file()
            and in_file.suffix.lower() in [".png", ".jpg", ".jpeg"]
            and shop_name in in_file.stem
        ):
            png_file_list.append(in_file)

    pil_list = []
    for file in png_file_list:
        file: Path
        im = Image.open(file.as_posix())
        im = im.convert("RGBA")
        pil_list.append(im)

    avera_ratio = sum([pil.width / pil.height for pil in pil_list]) / len(pil_list)

    for pil in pil_list:
        pil.thumbnail((800, 800))

    if avera_ratio < 1:
        bg = fun_图片横向拼接(
            image_list=pil_list,
            spacing=10,
            align_item="center",
            background_color=(255, 255, 255, 255),
        )
    else:
        bg = fun_图片竖向拼接(
            image_list=pil_list,
            spacing=10,
            align_item="center",
            background_color=(255, 255, 255, 255),
        )

    pic_path = sub_path.parent / (sub_path.stem + ".png")

    bg.save(pic_path.as_posix())
