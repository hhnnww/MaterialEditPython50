"""解压ZIP文件"""

from pathlib import Path
from zipfile import BadZipfile, ZipFile


def fun_unzip_file(file_path: Path) -> None:
    """解压zip文件"""
    try:
        with ZipFile(file=file_path, mode="r") as z:
            z.extractall((file_path.parent / file_path.stem).as_posix())
    except BadZipfile:
        print("损坏的文件:\t" + file_path.as_posix())
    else:
        file_path.unlink()
