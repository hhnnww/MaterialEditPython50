import shutil
from pathlib import Path

from tqdm import tqdm

from ..setting import IMAGE_SUFFIX


def fun_复制到预览图(folder: str, preview_path: str):
    folder_obj = Path(folder)
    preview_path_obj = Path(preview_path)

    if preview_path_obj.exists() is False:
        preview_path_obj.mkdir()

    # 构建图片列表
    pic_list = []
    for in_file in folder_obj.rglob("*"):
        if in_file.is_file() and in_file.suffix.lower() in IMAGE_SUFFIX:
            if in_file.parent.stem != "Links":
                pic_list.append(in_file)

    # 遍历图片
    for in_file in tqdm(pic_list, ncols=100, desc="复制到预览图\t"):
        in_file: Path

        # 转换成预览图路径
        preview_path_text = in_file.as_posix().replace(
            folder_obj.as_posix(), preview_path_obj.as_posix()
        )
        preview_img_path_obj = Path(preview_path_text)

        # 如果预览图在子文件夹内，创建子文件夹
        if preview_img_path_obj.exists() is False:
            if preview_img_path_obj.parent.exists() is False:
                preview_img_path_obj.parent.mkdir(parents=True)

            # 开始复制
            shutil.copy(in_file.as_posix(), preview_img_path_obj)
