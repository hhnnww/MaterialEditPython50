import shutil
from pathlib import Path


def fun_删除文件夹(folder: str):
    if Path(folder).exists() is True and Path(folder).is_dir():
        shutil.rmtree(folder)
