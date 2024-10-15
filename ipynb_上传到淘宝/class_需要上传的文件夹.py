from pathlib import Path


class Cla_需要上传的文件夹:
    def __init__(self, start_path_str: str) -> None:
        self.start_path = Path(start_path_str)

    @property
    def fun_shop_name(self) -> str:
        return self.start_path.parts[1]

    @property
    def __fun_start_num(self) -> int:
        return int(self.start_path.stem)

    @staticmethod
    def __fun_获取文件夹NUM(path_obj: Path) -> int:
        try:
            return int(path_obj.stem)
        except ValueError:
            return 0

    @property
    def __parnet_path(self) -> Path:
        return self.start_path.parent

    @property
    def fun_所有文件夹(self) -> list[Path]:
        all_path = []
        for in_path in self.__parnet_path.iterdir():
            if (
                in_path.is_dir()
                and self.__fun_获取文件夹NUM(in_path) >= self.__fun_start_num
            ):
                all_path.append(in_path)

        all_path.sort(key=lambda k: self.__fun_获取文件夹NUM(k))

        return all_path

    @property
    def fun_所有文件夹ID(self) -> list[int]:
        return [self.__fun_获取文件夹NUM(k) for k in self.fun_所有文件夹]


if __name__ == "__main__":
    obj = Cla_需要上传的文件夹(start_path_str=r"F:\小夕素材\10000-20000\10730")
    print(obj.fun_所有文件夹ID)
