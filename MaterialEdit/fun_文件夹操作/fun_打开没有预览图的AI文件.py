"""open no png ai file"""

from functools import cached_property
from pathlib import Path

from win32com.client import Dispatch

from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob
from MaterialEdit.setting import IMAGE_SUFFIX


class OpenNoPngAIFile:
    def __init__(self, in_path: str) -> None:
        """打开没有预览图的AI文件"""
        self.material_path = Path(in_path)
        self.all_ai_file = rglob(in_path, suffix=[".ai"])

    open_ai_file_num = 10

    def main(self) -> None:
        """开始运行"""
        app = Dispatch("Illustrator.Application")
        num = 0
        for ai_file in self.all_ai_file:
            ai_file_obj = AIFile(ai_file=ai_file)
            if ai_file_obj.has_png is False:
                app.Open(ai_file.as_posix())

                num += 1

                if num == self.open_ai_file_num:
                    return


class AIFile:
    def __init__(self, ai_file: Path) -> None:
        """Init"""
        self.ai_file = ai_file

    @cached_property
    def all_png(self) -> list[Path]:
        """AI同目录下的所有图片文件"""
        return [
            in_file
            for in_file in self.ai_file.parent.iterdir()
            if in_file.is_file() and in_file.suffix.lower() in IMAGE_SUFFIX
        ]

    @property
    def has_png(self) -> bool:
        """遍历所有图片

        如果ai文件的stem在图片的stem
        返回True
        不然返回False
        """
        return any(self.ai_file.stem in in_file.name for in_file in self.all_png)


if __name__ == "__main__":
    open_ai = OpenNoPngAIFile(in_path=r"F:\小夕素材\10000-20000\10938\10938")
    open_ai.main()
