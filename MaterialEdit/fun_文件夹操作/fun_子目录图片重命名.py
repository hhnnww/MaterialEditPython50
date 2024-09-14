from pathlib import Path
from uuid import uuid4


def fun_子目录图片重命名(material_path: str):
    # 内目录重命名
    def __fun_内目录重命名(in_path: Path):
        # 改成UUID
        for in_file in in_path.iterdir():
            if in_file.is_file() and in_file.suffix.lower() in [
                ".jpg",
                ".jpeg",
                ".png",
            ]:
                in_file.rename(in_file.with_stem(str(uuid4)))

        # 改名
        num = 0
        for in_file in in_path.iterdir():
            if in_file.is_file() and in_file.suffix.lower() in [
                ".jpg",
                ".jpeg",
                ".png",
            ]:
                if num == 0:
                    new_path = in_file.with_stem(in_path.stem)
                else:
                    new_path = in_file.with_stem(f"{in_path.stem}_{num}")

                in_file.rename(new_path)
                num += 1

    # 大文件夹改名
    for in_path in Path(material_path).iterdir():
        if in_path.is_dir():
            __fun_内目录重命名(in_path=in_path)
