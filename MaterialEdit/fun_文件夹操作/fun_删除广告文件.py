from pathlib import Path

from ..setting import AD_SUFFIX


def fun_删除广告文件(folder: str):
    folder_obj = Path(folder)

    for in_file in folder_obj.rglob("*"):
        if in_file.is_file():
            if in_file.suffix.lower() in AD_SUFFIX:
                in_file.unlink()

            elif in_file.stem[:2] == "._" and in_file.stat().st_size < 300:
                in_file.unlink()

            elif in_file.stat().st_size == 0:
                in_file.unlink()

            elif in_file.stem.lower() == ".ds_store":
                in_file.unlink()
