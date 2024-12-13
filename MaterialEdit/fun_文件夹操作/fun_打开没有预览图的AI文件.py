from functools import cached_property
from pathlib import Path

from win32com.client import Dispatch

from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import fun_遍历指定文件
from MaterialEdit.setting import IMAGE_SUFFIX


class OpenNoPngAIFile:
    def __init__(self, in_path: str) -> None:
        self.material_path = Path(in_path)
        self.all_ai_file = fun_遍历指定文件(in_path, suffix=[".ai"])

    def main(self):
        app = Dispatch("Illustrator.Application")
        num = 0
        for ai_file in self.all_ai_file:
            ai_file_obj = AIFile(ai_file=ai_file)
            if ai_file_obj.has_png is False:
                print(f"打开文件{ai_file.as_posix()}")
                # os.startfile(ai_file.as_posix())
                app.Open(ai_file.as_posix())

                num += 1

                if num == 5:
                    return


class AIFile:
    def __init__(self, ai_file: Path) -> None:
        self.ai_file = ai_file

    @cached_property
    def all_png(self) -> list[Path]:
        # AI同目录下的所有图片文件
        all_file = []
        for in_file in self.ai_file.parent.iterdir():
            if in_file.is_file() and in_file.suffix.lower() in IMAGE_SUFFIX:
                all_file.append(in_file)

        return all_file

    @property
    def has_png(self):
        """
        遍历所有图片
        如果ai文件的stem在图片的stem
        返回True
        不然返回False
        """
        for in_file in self.all_png:
            if self.ai_file.stem in in_file.name:
                return True

        return False


if __name__ == "__main__":
    open_ai = OpenNoPngAIFile(in_path=r"F:\小夕素材\10000-20000\10938\10938")
    open_ai.main()
