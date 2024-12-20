"""打开没有生成PNG图片的PSD文档."""

from pathlib import Path

from win32com.client import Dispatch

from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob
from MaterialEdit.setting import IMAGE_SUFFIX


class OpenPsdOneFile:
    """判断psd是否包含图片."""

    def __init__(self, psd_file: Path) -> None:
        """传入PSD文件."""
        self.psd_file = psd_file

    def has_image(self) -> bool:
        """判断这个PSD是否生成了图片文件."""
        for suffix in IMAGE_SUFFIX:
            png_path = self.psd_file.with_suffix(suffix=suffix)
            if png_path.exists() is True:
                return True

        return False


class OpenNoImagePsdFiles:
    """打开所有没有预览图的PSD."""

    def __init__(self, material_path: str) -> None:
        """传入素材文件夹."""
        self.material_path = Path(material_path)

    def main(self) -> None:
        """遍历PSD 没有预览图的打开5个."""
        app = Dispatch(dispatch="photoshop.application")
        num = 0
        open_num = 5
        for psd_file in rglob(
            folder=self.material_path.as_posix(),
            suffix=[".psd", ".psb"],
        ):
            psd_obj = OpenPsdOneFile(psd_file=psd_file)
            if psd_obj.has_image() is False:
                app.Open(psd_file.as_posix())
                num += 1

                if num == open_num:
                    return
