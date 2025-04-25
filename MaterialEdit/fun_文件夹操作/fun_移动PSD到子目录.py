from pathlib import Path

from mylog import mylogger


def fun_移动PSD到子目录(material_path: str) -> None:
    """移动PSD文件到子目录."""
    for infile in Path(material_path).rglob("*"):
        mylogger.info(f"正在处理文件: {infile}")
        if infile.is_file() and infile.suffix.lower() in [".psd", ".psb"]:
            sub_path = Path(material_path) / infile.stem
            if not sub_path.exists():
                sub_path.mkdir()
            infile.rename(target=sub_path / infile.name)


if __name__ == "__main__":
    fun_移动PSD到子目录(
        r"F:\\小夕素材\11000-11999\11261\11261",
    )  # 替换为你的素材文件夹路径
