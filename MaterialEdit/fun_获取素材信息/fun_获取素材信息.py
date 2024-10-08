from pathlib import Path

from ..fun_创建文件夹结构 import fun_创建文件夹结构
from ..fun_遍历图片 import fun_遍历图片
from ..type import MaterialInfo
from .fun_获取所有尺寸 import fun_获取所有尺寸
from .fun_获取所有文件列表 import fun_获取所有文件列表
from .fun_获取源文件数量 import fun_获取源文件数量


def fun_获取素材信息(root_path: str, used_image: int, image_sort: bool):
    root_path_structure = fun_创建文件夹结构(root_path)

    material_id = Path(root_path).stem
    material_path = root_path_structure.material_path

    preview_image_path = root_path_structure.preview_path
    preview_image_list = [
        dict(path=obj)
        for obj in fun_遍历图片(
            folder=preview_image_path, image_sort=image_sort, used_image_number=0
        )
        if "_thumb" not in Path(obj).stem
    ]
    preview_image_count = len(preview_image_list)

    if used_image > 0:
        preview_image_list = preview_image_list[:used_image]

    effect_image_path = root_path_structure.effect_path
    effect_image_list = [
        dict(path=obj)
        for obj in fun_遍历图片(
            folder=effect_image_path, image_sort=image_sort, used_image_number=0
        )
        if "_thumb" not in Path(obj).stem
    ]

    all_file = fun_获取所有文件列表(root_path_structure.material_path)

    material_source_file_size = fun_获取所有尺寸(all_file)

    material_count_num_obj = fun_获取源文件数量(all_file)
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
