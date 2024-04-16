import shutil
from pathlib import Path

from tqdm import tqdm

from ..setting import IMAGE_SUFFIX


def fun_复制到预览图(folder: str, preview_path: str):
    folder_obj = Path(folder)
    preview_path_obj = Path(preview_path)

    if preview_path_obj.exists() is False:
        preview_path_obj.mkdir()

    pic_list = []
    for in_file in folder_obj.rglob("*"):
        if in_file.is_file() and in_file.suffix.lower() in IMAGE_SUFFIX:
            if in_file.parent.stem != "Links":
                pic_list.append(in_file)

    for in_file in tqdm(pic_list, ncols=100, desc="复制到预览图\t"):
        preview_path = in_file.as_posix().replace(folder_obj.as_posix(), preview_path_obj.as_posix())
        preview_path = Path(preview_path)

        if preview_path.exists() is False:
            if preview_path.parent.exists() is False:
                print(preview_path.parent)
                preview_path.parent.mkdir(parents=True)

            shutil.copy(in_file.as_posix(), preview_path)
