"""文件重命名.py"""

import shutil
from pathlib import Path


def fun_删除文件夹(folder: str) -> None:
    """删除文件夹."""
    if Path(folder).exists() is True and Path(folder).is_dir():
        shutil.rmtree(folder)
