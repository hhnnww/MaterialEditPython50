"""获取素材信息."""

from pathlib import Path

from MaterialEdit.fun_创建文件夹结构 import fun_创建文件夹结构
from MaterialEdit.fun_获取素材信息.get_all_material_file_size import (
    get_all_material_file_size,
)
from MaterialEdit.fun_获取素材信息.material_file_count import mateiral_file_count
from MaterialEdit.fun_获取素材信息.material_file_list import material_file_list
from MaterialEdit.fun_遍历图片 import fun_遍历图片
from MaterialEdit.type import MaterialInfo


def fun_获取素材信息(root_path: str, used_image: int, image_sort: bool) -> MaterialInfo:
    """获取素材文件夹信息."""
    root_path_structure = fun_创建文件夹结构(root_path=root_path)

    material_id = Path(root_path).stem
    material_path = root_path_structure.material_path

    preview_image_path = root_path_structure.preview_path
    preview_image_list = [
        {"path": obj}
        for obj in fun_遍历图片(
            folder=preview_image_path,
            image_sort=image_sort,
            used_image_number=0,
        )
        if "_thumb" not in Path(obj).stem
    ]
    preview_image_count = len(preview_image_list)

    if used_image > 0:
        preview_image_list = preview_image_list[:used_image]

    effect_image_path = root_path_structure.effect_path
    effect_image_list = [
        {"path": obj}
        for obj in fun_遍历图片(
            folder=effect_image_path,
            image_sort=image_sort,
            used_image_number=0,
        )
        if "_thumb" not in Path(obj).stem
    ]

    all_file = material_file_list(material_path=root_path_structure.material_path)

    material_source_file_size = get_all_material_file_size(all_file=all_file)

    material_count_num_obj = mateiral_file_count(file_list=all_file)
    material_count_num_obj.sort(key=lambda obj: obj[0], reverse=True)

    try:
        material_source_file_count = material_count_num_obj[0][0]
        material_source_format = material_count_num_obj[0][1]
    except IndexError:
        material_source_file_count = 0
        material_source_format = "none"

    material_source_format_number = (
        f"{material_source_file_count}个 {material_source_format} 文件"
    )

    material_source_format_title = ""
    if len(material_count_num_obj) > 0:
        first_suffix = material_count_num_obj[0][1]
        if first_suffix in ["psd", "psb"]:
            material_source_format_title = f"{first_suffix} 设计素材"
        elif first_suffix in ["ai", "eps"]:
            material_source_format_title = f"{first_suffix} 矢量设计素材"
        elif first_suffix in ["ppt", "pptx"]:
            material_source_format_title = f"{first_suffix} 幻灯片设计素材"
        elif first_suffix in ["otf", "ttf"]:
            material_source_format_title = f"{first_suffix} 字体文件素材"
        elif first_suffix in ["cdr"]:
            material_source_format_title = f"{first_suffix} 矢量素材"
        elif first_suffix in ["skp"]:
            material_source_format_title = "SU单体模型"

    return MaterialInfo(
        material_path=material_path.upper(),
        material_id=material_id.upper(),
        material_source_file_size=material_source_file_size.upper(),
        material_source_file_count=material_source_file_count,
        material_source_format=material_source_format.upper(),
        material_source_format_title=material_source_format_title.upper(),
        material_source_format_number=material_source_format_number.upper(),
        preview_image_path=preview_image_path,
        preview_image_count=preview_image_count,
        preview_image_list=preview_image_list,
        effect_image_path=effect_image_path,
        effect_image_list=effect_image_list,
    )
