"""AI文件移动到子目录"""

from pathlib import Path


def fun_AI文件移动到子目录(material_path: Path) -> None:
    """AI文件移动到子目录"""
    for in_file in material_path.iterdir():
        if in_file.is_file() and in_file.suffix.lower() in [".ai", ".eps"]:
            new_path = material_path / in_file.stem / in_file.name

            if new_path.parent.exists() is not True:
                new_path.parent.mkdir()

            in_file.rename(new_path)


if __name__ == "__main__":
    fun_AI文件移动到子目录(
        Path(r"F:\小夕素材\H000-H999\H0707\H0707"),
    )
