from pathlib import Path


class AI_批量导出图片重命名:
    def __init__(self, ai_file: Path) -> None:
        self.ai_file = ai_file

    @property
    def fun_all_jpg_file(self) -> list[Path]:
        jpg_list = []
        for in_file in self.ai_file.parent.iterdir():
            if (
                in_file.is_file()
                and in_file.suffix.lower() in [".jpg"]
                and self.ai_file.stem in in_file.stem
            ):
                jpg_list.append(in_file)

        return jpg_list

    def fun_jpg_重命名(self):
        for num, in_file in enumerate(self.fun_all_jpg_file):
            in_file: Path
            if num == 0:
                new_path = in_file.with_stem(self.ai_file.stem)
            else:
                new_path = in_file.with_stem(f"{self.ai_file.stem}_{num+1}")

            if new_path.exists() is False:
                in_file.rename(new_path)


if __name__ == "__main__":
    for in_file in Path(r"F:\BaiduNetdiskDownload\4417\4417").iterdir():
        if in_file.is_file() and in_file.suffix.lower() in [".ai"]:
            ai_obj = AI_批量导出图片重命名(in_file)
            print(ai_obj.fun_jpg_重命名())
