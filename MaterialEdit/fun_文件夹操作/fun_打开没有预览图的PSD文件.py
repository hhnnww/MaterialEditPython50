from pathlib import Path

from win32com.client import Dispatch

from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import fun_遍历指定文件
from MaterialEdit.setting import IMAGE_SUFFIX


class OpenPsdOneFile:
    def __init__(self, psd_file: Path) -> None:
        self.psd_file = psd_file

    def has_image(self) -> bool:
        for suffix in IMAGE_SUFFIX:
            png_path = self.psd_file.with_suffix(suffix=suffix)
            if png_path.exists() is True:
                return True

        return False


class OpenNoImagePsdFiles:
    def __init__(self, material_path: str) -> None:
        self.material_path = Path(material_path)

    def main(self) -> None:
        app = Dispatch(dispatch="photoshop.application")
        num = 0
        for psd_file in fun_遍历指定文件(
            folder=self.material_path.as_posix(), suffix=[".psd", ".psb"]
        ):
            psd_obj = OpenPsdOneFile(psd_file=psd_file)
            if psd_obj.has_image() is False:
                app.Open(psd_file.as_posix())
                num += 1

                if num == 5:
                    return
