from pathlib import Path


def fun_同层级图片改名(ai_path: Path) -> None:
    for in_file in ai_path.parent.iterdir():
        if (
            in_file.is_file()
            and in_file.suffix.lower() in [".png", ".jpg", ".jpeg"]
            and "export_" in in_file.stem
        ):
            new_name = in_file.with_stem(ai_path.stem)

            num = 1
            while new_name.exists() is True:
                new_name = in_file.with_stem(f"{ai_path.stem}_{num}")
                num += 1

            in_file.rename(new_name)
