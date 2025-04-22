from functools import cached_property
from pathlib import Path


class AIBatchExportImageRename:
    """批量导出图片重命名."""

    def __init__(self, ai_file: Path) -> None:
        """Batch export image rename."""
        self.ai_file = ai_file

    @cached_property
    def __all_file(self) -> list[Path]:
        return [
            in_file
            for in_file in self.ai_file.parent.iterdir()
            if in_file.is_file() and in_file.suffix.lower() in [".jpg", ".png"]
        ]

    @property
    def fun_all_jpg_file(self) -> list[Path]:
        """获取所有jpg文件"""
        return [
            in_file for in_file in self.__all_file if self.ai_file.stem in in_file.stem
        ]

    def fun_jpg_重命名(self) -> None:
        """重命名jpg文件"""
        for num, in_file in enumerate(self.fun_all_jpg_file):
            in_file: Path
            if num == 0:
                new_path = in_file.with_stem(self.ai_file.stem)
            else:
                new_path = in_file.with_stem(f"{self.ai_file.stem}_{num + 1}")

            if new_path.exists() is False:
                in_file.rename(new_path)


if __name__ == "__main__":
    for in_file in Path(r"F:\BaiduNetdiskDownload\4417\4417").iterdir():
        if in_file.is_file() and in_file.suffix.lower() in [".ai"]:
            ai_obj = AIBatchExportImageRename(in_file)
            print(ai_obj.fun_jpg_重命名())
