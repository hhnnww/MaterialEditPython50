from pathlib import Path

from PIL import Image

from ..fun_图片编辑 import ImageEdit


def fun_享设计制作预览图(material_path: str, shop_name: str):
    for sub_path in Path(material_path).iterdir():
        if sub_path.is_dir():
            fun_制作文件夹大图(sub_path=sub_path, shop_name=shop_name)


def fun_制作文件夹大图(sub_path: Path, shop_name: str):
    png_file_list = []
    for in_file in sub_path.iterdir():
        if in_file.is_file() and in_file.suffix.lower() in [".png"] and shop_name in in_file.stem:
            png_file_list.append(in_file)

    pil_list = [Image.open(in_file.as_posix()) for in_file in png_file_list]
    avera_ratio = sum([pil.width / pil.height for pil in pil_list]) / len(pil_list)

    for pil in pil_list:
        pil.thumbnail((800, 800))

    pil_list = [
        ImageEdit.fun_图片切换到圆角(im=pil, border_radius=10, background_color=(255, 255, 255, 255)) for pil in pil_list
    ]

    if avera_ratio < 1:
        bg = ImageEdit.fun_图片横向拼接(
            image_list=pil_list, spacing=10, align_item="center", background_color=(255, 255, 255, 255)
        )
    else:
        bg = ImageEdit.fun_图片竖向拼接(
            image_list=pil_list, spacing=10, align_item="center", background_color=(255, 255, 255, 255)
        )

    bg = ImageEdit.fun_图片扩大粘贴(
        im=bg,
        width=bg.width + 20,
        height=bg.height + 20,
        left="center",
        top="center",
        background_color=(255, 255, 255, 255),
    )

    pic_path = sub_path.parent / (sub_path.stem + ".png")

    bg.save(pic_path.as_posix())
