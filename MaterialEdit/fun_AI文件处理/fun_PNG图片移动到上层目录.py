from pathlib import Path
import shutil


def fun_PNG图片移动到上层目录(ai_path: Path):
    # 移动到上层目录
    # png_path = ai_path.parent / "3000w"
    png_path_list = [ai_path.parent / "3000w", ai_path.parent / "1500w"]

    for p in png_path_list:
        if p.exists() is True:
            png_file_list = []
            for in_file in p.iterdir():
                if in_file.is_file() and in_file.suffix.lower() == ".png":
                    png_file_list.append(in_file)

            num = 1
            for in_file in png_file_list:
                new_name = ai_path.with_suffix(".png")

                while new_name.exists() is True:
                    new_name = ai_path.with_suffix(".png").with_stem(f"{ai_path.stem}_{num + 1}")
                    num += 1

                in_file.rename(new_name)

            shutil.rmtree(p.as_posix())
