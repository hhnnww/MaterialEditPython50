"""文件重命名.py"""

from pathlib import Path

from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接


def fun_享设计制作预览图(material_path: str, shop_name: str) -> None:
    """根据指定文件夹路径和店铺名称，生成包含所有符合条件图片的大图，并保存到文件夹的上一级目录。"""
    for sub_path in Path(material_path).iterdir():
        if sub_path.is_dir():
            fun_制作文件夹大图(sub_path=sub_path, shop_name=shop_name)


def fun_制作文件夹大图(sub_path: Path, shop_name: str) -> None:
    """根据指定文件夹路径和店铺名称，生成包含所有符合条件图片的大图，并保存到文件夹的上一级目录。

    参数:
        sub_path (Path): 包含图片的子文件夹路径。
        shop_name (str): 用于筛选图片的店铺名称关键字。
    功能描述:
        1. 从指定文件夹中筛选出包含店铺名称关键字的图片文件
        （支持 .png, .jpg, .jpeg 格式）。
        2. 计算所有图片的平均宽高比。
        3. 根据宽高比决定拼接方式：
           - 如果宽高比小于 1 则横向拼接图片。
           - 如果宽高比大于等于 1 则竖向拼接图片。
        4. 拼接后的图片保存为 PNG 格式，文件名与子文件夹名称相同，存储在上一级目录。
    注意:
        - 图片会被缩放至最大宽高为 2000 像素。
        - 拼接时图片之间会有 10 像素的间距，背景为白色。
    """
    png_file_list = [
        in_file
        for in_file in sub_path.iterdir()
        if (
            in_file.is_file()
            and in_file.suffix.lower() in [".png", ".jpg", ".jpeg"]
            and shop_name in in_file.stem
        )
    ]

    pil_list = []
    for file in png_file_list:
        file: Path
        im = Image.open(file.as_posix())
        im = im.convert("RGBA")
        pil_list.append(im)

    avera_ratio = sum([pil.width / pil.height for pil in pil_list]) / len(pil_list)

    for pil in pil_list:
        pil.thumbnail((2000, 2000))

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
