"""压缩图片"""

from pathlib import Path

import pythoncom
from PIL import Image
from tqdm import tqdm
from win32com.client import Dispatch

from MaterialEdit.setting import IMAGE_SUFFIX

Image.MAX_IMAGE_PIXELS = None


def __fun_压缩单个图片(image_path: Path) -> None:
    ps_app = Dispatch("Photoshop.Application")
    ps_app.displayDialogs = 3
    ps_app.Open(image_path.as_posix())
    doc = ps_app.activeDocument

    options = Dispatch("Photoshop.ExportOptionsSaveForWeb")
    options.Format = 6
    options.Quality = 60

    jpg_path = image_path.with_suffix(".jpg")
    doc.Export(ExportIn=jpg_path.as_posix(), ExportAs=2, Options=options)

    if image_path.suffix.lower() == ".png":
        image_path.unlink()

    doc.Close(2)


def fun_图片压缩(material_path: str) -> None:
    """压缩指定文件夹中超过最大大小的图片文件 并将其保存为JPEG格式。"""
    pythoncom.CoInitialize()
    max_size = 20
    for infile in tqdm(
        [
            infile
            for infile in Path(material_path).rglob("*")
            if infile.is_file()
            and infile.parent.stem.lower() != "links"
            and infile.suffix.lower() in IMAGE_SUFFIX
            and infile.stat().st_size / 1000 / 1000 > max_size
        ],
        desc="压缩图片",
        unit="个",
        ncols=100,
    ):
        __fun_压缩单个图片(infile)

    pythoncom.CoUninitialize()
