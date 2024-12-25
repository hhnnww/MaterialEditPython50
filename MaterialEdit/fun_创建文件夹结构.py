"""创建素材文件夹结构."""

from __future__ import annotations

from pathlib import Path

from MaterialEdit.type import _FolderStructure


def fun_创建文件夹结构(root_path: str | Path) -> _FolderStructure:
    """创建素材文件夹结构."""
    root_path_obj = Path(root_path)

    if root_path_obj.stem == root_path_obj.parent.stem:
        msg = "素材根目录不能和父母路的stem相同"
        raise IndexError(msg)

    if root_path_obj.is_absolute() is not True:
        msg = "素材根目录必须是绝对路径"
        raise IndexError(msg)

    path_parts_count = 3
    if len(root_path_obj.parts) < path_parts_count:
        msg = "素材根目录层级必须大于3"
        raise IndexError(msg)

    if "-" in root_path_obj.stem:
        msg = "素材目录不能包含 -"
        raise IndexError(msg)

    material_path = root_path_obj / root_path_obj.stem
    if material_path.exists() is False:
        material_path.mkdir(parents=True)

    preview_path = root_path_obj / "预览图"
    effect_path = root_path_obj / "效果图"
    ori_img_path = root_path_obj / "原始图"
    design_path = root_path_obj / "设计图"

    return _FolderStructure(
        root_path=root_path_obj.as_posix(),
        material_path=material_path.as_posix(),
        preview_path=preview_path.as_posix(),
        effect_path=effect_path.as_posix(),
        ori_img_path=ori_img_path.as_posix(),
        design_path=design_path.as_posix(),
    )
