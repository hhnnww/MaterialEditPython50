"""素材基本功能."""

import logging
import re
import shutil
from pathlib import Path
from typing import ClassVar

from colorama import Fore, Style

logging.basicConfig(
    level=logging.INFO,
    format=f"{Fore.YELLOW}%(levelname)s{Style.RESET_ALL}:\t%(asctime)s - %(message)s",
)


class MaterialType:
    material_suffix: ClassVar[list[str]] = [
        ".ai",
        ".eps",
        ".psd",
        ".psb",
        ".su",
        ".ppt",
        ".pptx",
    ]
    image_suffix: ClassVar[list[str]] = [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp",
    ]
    zip_suffix: ClassVar[list[str]] = [".zip", ".rar", ".7z"]
    ad_suffix: ClassVar[list[str]] = [
        ".txt",
        ".url",
        ".html",
        ".htm",
        ".doc",
        ".docx",
        ".pdf",
        ".psd_exiftool_tmp",
    ]

    @staticmethod
    def fun_获取文件名中的数字(stem: str) -> int:
        """获取文件名中的数字."""
        int_find = re.findall(r"\d+", stem)
        if len(int_find) == 0:
            return 0

        return int("".join(int_find))

    @staticmethod
    def fun_移动到根目录(folder: Path) -> None:
        """素材移动到根目录."""
        # 移动所有文件
        for infile in folder.rglob("*"):
            if infile.parent != folder:
                new_path = MaterialType.fun_路径去重(folder / infile.name)
                infile.rename(target=new_path)

        # 删除空文件夹
        for infile in folder.iterdir():
            if infile.is_dir():
                shutil.rmtree(infile)

    @staticmethod
    def fun_路径去重(path: Path) -> Path:
        """路径去重."""
        if path.exists() is not True:
            return path

        num = 0
        new_path = path
        while new_path.exists():
            new_path = path.with_stem(f"{path.stem}_{num}")
            num += 1
        return new_path

    @staticmethod
    def log(msg: str) -> None:
        """打印输出."""
        logging.info(msg=msg)
