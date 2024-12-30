"""导出PNG."""

from pathlib import Path

from win32com.client import Dispatch

from fun_素材文件夹 import material_base_func


class AiFile:
    def __init__(self, path: Path) -> None:
        """AI文件."""
        material_base_func.MaterialType.log(f"打开{path.as_posix()}")
        self.path = path
        self.app = Dispatch("illustrator.Application")
        self.doc = self.app.Open(self.path)

    def main(self) -> None:
        """开始操作."""
        material_base_func.MaterialType.log(f"开始操作{self.path.as_posix()}")
        self.app.DoJavaScriptFile(r"F:\codeProject\AdobeJSX\illustrator.jsx")


if __name__ == "__main__":
    AiFile(path=Path(r"F:\小夕素材\11000-11999\11014\11014\小夕素材(1).ai")).main()
