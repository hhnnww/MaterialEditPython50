import shutil
from pathlib import Path

from mylog import mylogger


def fun_删除IMAGE文件夹(material_path: str) -> None:
    for in_path in Path(material_path).rglob(pattern="*"):
        if in_path.is_dir() and in_path.stem == "images":
            shutil.rmtree(in_path, ignore_errors=True)
            mylogger.info(msg=f"删除文件夹: {in_path}")
