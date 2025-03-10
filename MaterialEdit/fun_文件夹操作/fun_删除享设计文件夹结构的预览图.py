from pathlib import Path

from MaterialEdit.setting import IMAGE_SUFFIX


def fun_删除享设计文件夹结构的预览图(material_path: Path) -> None:
    """删除享设计文件夹结构的预览图"""
    for in_file in material_path.iterdir():
        if in_file.is_file() and in_file.suffix.lower() in IMAGE_SUFFIX:
            in_file.unlink()

    for sub_path in material_path.iterdir():
        if sub_path.is_dir():
            for in_file in sub_path.iterdir():
                if in_file.is_file() and in_file.suffix.lower() in IMAGE_SUFFIX:
                    in_file.unlink()


if __name__ == "__main__":
    fun_删除享设计文件夹结构的预览图(
        material_path=Path(r"F:\小夕素材\H000-H999\H0707\H0707"),
    )
