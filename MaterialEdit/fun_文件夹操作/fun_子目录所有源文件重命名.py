from pathlib import Path
from uuid import uuid4


def __fun_子目录重命名(in_path: Path) -> None:
    """子目录重命名"""
    # 获取所有源文件
    all_file = [
        in_file
        for in_file in in_path.iterdir()
        if in_file.is_file() and in_file.suffix.lower() in [".ai", ".psd", ".psb"]
    ]
    all_file.sort(key=lambda x: x.suffix.lower())
    uuid_str = str(uuid4())
    for num, infile in enumerate(all_file):
        new_path = infile.with_stem(f"{uuid_str}_{num}")
        if not new_path.exists():
            infile.rename(new_path)

    # 重命名后 重新命名文件夹
    all_file = [
        in_file
        for in_file in in_path.iterdir()
        if in_file.is_file() and in_file.suffix.lower() in [".ai", ".psd", ".psb"]
    ]
    all_file.sort(key=lambda x: x.suffix.lower())
    new_name = in_path.stem
    for num, infile in enumerate(all_file):
        new_path = infile.with_stem(f"{new_name}_{num + 1}")
        if not new_path.exists():
            infile.rename(new_path)


def fun_子目录所有源文件重命名(material_path: str) -> None:
    """子目录所有源文件重命名"""
    for in_path in Path(material_path).iterdir():
        if in_path.is_dir():
            __fun_子目录重命名(in_path)
