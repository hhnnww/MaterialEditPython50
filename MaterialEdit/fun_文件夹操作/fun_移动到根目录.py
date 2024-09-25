import shutil
from pathlib import Path

from tqdm import tqdm


def fun_移动到根目录(folder: str):
    folder_obj = Path(folder)

    if "Thumbs" in folder_obj.stem:
        return

    for in_file in tqdm(list(folder_obj.rglob("*")), ncols=100, desc="移动到根目录"):
        if in_file.is_file() and in_file.parent != folder_obj:
            new_path = folder_obj / in_file.name

            num = 1
            while new_path.exists() is True:
                new_path = folder_obj / f"{in_file.stem}_{num}{in_file.suffix}"
                num += 1

            shutil.move(in_file.as_posix(), new_path.as_posix())

    for in_file in folder_obj.iterdir():
        if in_file.is_dir() and "Thumbs" not in in_file.name:
            shutil.rmtree(in_file.as_posix())
