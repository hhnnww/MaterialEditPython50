import shutil
from pathlib import Path

from tqdm import tqdm

from .fun_创建文件夹结构 import fun_创建文件夹结构
from .get_stem_num import get_path_num
from .setting import IMAGE_SUFFIX, MATERIAL_SOURCE_SUFFIX
from .type import _FolderStructure


def fun_素材文件夹合并(ori_path: str, dst_path: str, shop_name: str):
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
