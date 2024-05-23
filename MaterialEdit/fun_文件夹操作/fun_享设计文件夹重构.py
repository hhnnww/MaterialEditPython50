import shutil
from pathlib import Path


def fun_享设计文件夹重构(material_path: str):
    for in_path in Path(material_path).iterdir():
        if in_path.is_dir():
            fun_单个文件夹重构(in_material_path=in_path)


def fun_单个文件夹重构(in_material_path: Path):
    links_path = in_material_path / "Links"
    # font_path = in_material_path / "Fonts"

    for in_file in in_material_path.rglob("*"):
        if in_file.is_file() and in_file.suffix.lower() not in [".ai", ".eps"]:
            # 如果是字体文件，移动到字体目录
            if in_file.suffix.lower() in [".otf", ".ttf", ".woff", ".woff2"]:
                windows_font_folder_path = Path(r"C:\Windows\fonts")
                windows_font_path = windows_font_folder_path / in_file.name

                if windows_font_path.exists() is False:
                    shutil.move(in_file, windows_font_path)

                in_file.unlink()

                # if font_path.exists() is False:
                #     font_path.mkdir()
                #
                # font_file_path = font_path / in_file.name
                #
                # if font_file_path.exists() is False:
                #     in_file.rename(font_file_path)

            # 如果不是字体文件，全部移动到Links目录
            else:
                if links_path.exists() is False:
                    links_path.mkdir()

                new_path = links_path / in_file.name
                if new_path.exists() is False:
                    in_file.rename(new_path)

    # 只要是空文件夹，全部删除。
    for in_path in in_material_path.iterdir():
        if in_path.is_dir() and len(list(in_path.iterdir())) == 0:
            in_path.unlink(missing_ok=True)


if __name__ == "__main__":
    fun_单个文件夹重构(Path(r"E:\小夕素材\10000-20000\10250\10250\小夕素材(02)"))
