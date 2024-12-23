"""初始化一个素材文件夹."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from MaterialEdit.fun_创建文件夹结构 import fun_创建文件夹结构

if TYPE_CHECKING:
    from MaterialEdit.type import _FolderStructure


def fun_文件夹初始化(root_path: str | Path) -> _FolderStructure:
    """初始化一个素材文件夹."""
    path_structures = fun_创建文件夹结构(root_path=root_path)

    root_path_obj = Path(path_structures.root_path)
    material_path_obj = Path(path_structures.material_path)
    preview_path_obj = Path(path_structures.preview_path)
    effect_path_obj = Path(path_structures.effect_path)
    ori_img_path_obj = Path(path_structures.ori_img_path)
    design_path_obj = Path(path_structures.design_path)

    if material_path_obj.exists() is False:
        material_path_obj.mkdir()

    for in_file in root_path_obj.iterdir():
        if in_file.is_dir() and in_file not in [
            material_path_obj,
            preview_path_obj,
            effect_path_obj,
            ori_img_path_obj,
            design_path_obj,
        ]:
            new_path = material_path_obj / in_file.name

            num = 1
            while new_path.exists() is True:
                new_path = new_path.with_name(new_path.name + str(num))
                num += 1
            shutil.move(in_file, new_path)

        if in_file.is_file():
            new_path = material_path_obj / in_file.name

            num = 1
            while new_path.exists() is True:
                new_path = new_path.with_stem(f"{new_path.stem}_{num}")
                num += 1

            shutil.move(in_file, new_path)

    return path_structures
