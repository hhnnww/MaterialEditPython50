"""制作详情"""

from pathlib import Path

from PIL import Image
from tqdm import tqdm

from MaterialEdit.fun_制作详情.fun_2_构建图片 import fun_构建图片
from MaterialEdit.fun_制作详情.fun_3_图片编组 import fun_图片编组
from MaterialEdit.fun_制作详情.fun_4_单行图片制作 import fun_单行图片制作
from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.setting import MATERIAL_SOURCE_SUFFIX
from MaterialEdit.type import ALIGNITEM


def fun_制作详情(
    image_path_list: list[str],
    line_number: int,
    max_line_ratio: float,
    contains_info: bool,
    material_path: str,
    crop_position: ALIGNITEM,
    shop_name: str,
    xq_width: int = 1500,
) -> Image.Image:
    image_list = fun_构建图片(image_list=image_path_list)
    comb_image_list = fun_图片编组(
        image_list,
        line_number=line_number,
        max_line_ratio=max_line_ratio,
    )

    material_fil_list = []
    if contains_info is True:
        material_fil_list = [
            obj
            for obj in list(Path(material_path).rglob("*"))
            if obj.is_file() and obj.suffix.lower() in MATERIAL_SOURCE_SUFFIX
        ]

    comb_pil_list = []
    for comb_image in tqdm(comb_image_list, ncols=100, desc="制作详情\t"):
        im = fun_单行图片制作(
            image_list=comb_image,
            contains_info=contains_info,
            material_file_list=material_fil_list,
            spacing=20,
            crop_position=crop_position,
            xq_width=xq_width,
            shop_name=shop_name,
        )
        comb_pil_list.append(im)

    spacing = 0

    if contains_info:
        spacing = 180

    im = fun_图片竖向拼接(
        image_list=comb_pil_list,
        spacing=spacing,
        align_item="center",
        background_color=(255, 255, 255, 255),
    )

    im = im.crop((0, 0, xq_width, im.height))

    return fun_图片扩大粘贴(
        background_color=(255, 255, 255, 255),
        height=im.height + 200,
        width=xq_width,
        im=im,
        left="center",
        top="start",
    )
