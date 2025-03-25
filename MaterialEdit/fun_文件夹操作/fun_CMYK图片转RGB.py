"""CMYK转RGB."""

from PIL import Image
from tqdm import tqdm
from win32com.client import Dispatch

from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob
from MaterialEdit.setting import IMAGE_SUFFIX


def fun_CMYK转RGB(material_path: str) -> None:
    """CMYK转RGB."""
    app = Dispatch("Photoshop.Application")
    for in_file in tqdm(
        rglob(material_path, IMAGE_SUFFIX),
        desc="CMYK转RGB",
        ncols=100,
    ):
        if in_file.is_file() and in_file.suffix.lower() in IMAGE_SUFFIX:
            with Image.open(in_file.as_posix()) as im:
                mode = im.mode

            if mode == "CMYK":
                app.Open(in_file.as_posix())
                doc = app.ActiveDocument
                doc.ChangeMode(2)
                doc.Save()
                doc.Close(2)
