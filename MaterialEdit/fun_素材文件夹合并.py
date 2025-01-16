"""合并素材文件夹，将 ori_path 中的素材文件移动到 dst_path 中，并重命名文件。

参数:
    ori_path (str): 原始素材文件夹路径。
    dst_path (str): 目标素材文件夹路径。
    shop_name (str): 店铺名称，用于重命名文件。
返回:
    None
功能:
    - 创建原始和目标文件夹结构对象。
    - 找到目标文件夹中最大的编号，并在此基础上递增编号。
    - 遍历原始文件夹中的所有文件，检查文件后缀是否在 MATERIAL_SOURCE_SUFFIX 中。
    - 将符合条件的文件移动到目标文件夹中，并根据店铺名称和编号重命名文件。
    - 同时移动相关的图片文件和预览文件，并重命名。
"""

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from tqdm import tqdm

from MaterialEdit.fun_创建文件夹结构 import fun_创建文件夹结构
from MaterialEdit.get_stem_num import get_path_num
from MaterialEdit.setting import IMAGE_SUFFIX, MATERIAL_SOURCE_SUFFIX

if TYPE_CHECKING:
    from MaterialEdit.type import _FolderStructure


def fun_素材文件夹合并(ori_path: str, dst_path: str, shop_name: str) -> None:
    """合并素材文件夹."""
    ori_obj: _FolderStructure = fun_创建文件夹结构(root_path=ori_path)
    dst_obj: _FolderStructure = fun_创建文件夹结构(root_path=dst_path)

    # 找到 dst_path 的最大 num
    num = 1
    for in_file in Path(dst_obj.material_path).rglob("*"):
        if in_file.is_file():
            in_num = get_path_num(in_file.stem)
            num = max(in_num, num)

    num += 1

    # 遍历 ori_path 文件夹
    for in_file in tqdm(
        list(Path(ori_obj.material_path).rglob("*")),
        ncols=100,
        desc="素材合并\t",
    ):
        if in_file.is_file() and in_file.suffix.lower() in MATERIAL_SOURCE_SUFFIX:
            source_file_new_path = Path(
                in_file.as_posix().replace(
                    Path(ori_obj.material_path).as_posix(),
                    Path(dst_obj.material_path).as_posix(),
                ),
            ).with_stem(f"{shop_name}({num})")
            shutil.move(in_file.as_posix(), source_file_new_path.as_posix())

            for image_suffix in IMAGE_SUFFIX:
                image_path = in_file.with_suffix(image_suffix)
                if image_path.exists() is True:
                    image_path_new = Path(
                        image_path.as_posix().replace(
                            Path(ori_obj.material_path).as_posix(),
                            Path(dst_obj.material_path).as_posix(),
                        ),
                    ).with_stem(f"{shop_name}({num})")
                    if image_path_new.parent.exists() is False:
                        image_path_new.parent.mkdir(parents=True)
                    shutil.move(image_path.as_posix(), image_path_new.as_posix())

                preview_path = Path(
                    in_file.with_suffix(image_suffix)
                    .as_posix()
                    .replace(
                        Path(ori_obj.material_path).as_posix(),
                        Path(ori_obj.preview_path).as_posix(),
                    ),
                )
                if preview_path.exists() is True:
                    preview_path_new = Path(
                        preview_path.as_posix().replace(
                            Path(ori_obj.preview_path).as_posix(),
                            Path(dst_obj.preview_path).as_posix(),
                        ),
                    ).with_stem(f"{shop_name}({num})")
                    if preview_path_new.parent.exists() is False:
                        preview_path_new.parent.mkdir(parents=True)
                    shutil.move(preview_path.as_posix(), preview_path_new.as_posix())

            num += 1
