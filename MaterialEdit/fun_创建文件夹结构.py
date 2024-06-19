from pathlib import Path

from .type import _FolderStructure


def fun_创建文件夹结构(root_path: str):
    root_path_obj = Path(root_path)

    if root_path_obj.stem == root_path_obj.parent.stem:
        raise IndexError("素材根目录不能和父母路的stem相同")

    elif root_path_obj.is_absolute() is not True:
        raise IndexError("素材根目录必须是绝对路径")

    elif len(root_path_obj.parts) < 3:
        raise IndexError("素材根目录层级必须大于3")

    elif "-" in root_path_obj.stem:
        raise IndexError("素材目录不能包含 -")

    material_path = root_path_obj / root_path_obj.stem
    if material_path.exists() is False:
        material_path.mkdir(parents=True)

    preview_path = root_path_obj / "预览图"
    effect_path = root_path_obj / "效果图"

    return _FolderStructure(
        root_path=root_path_obj.as_posix(),
        material_path=material_path.as_posix(),
        preview_path=preview_path.as_posix(),
        effect_path=effect_path.as_posix(),
    )
