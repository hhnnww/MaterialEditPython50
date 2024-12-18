"""构建需要上传的文件夹"""

from pathlib import Path


class MakeUsedFolder:
    """
    构建需要上传的文件夹
    """

    def __init__(self, start_path_str: str, end_num: int) -> None:
        self.start_path = Path(start_path_str)
        self.end_num = end_num

    @property
    def fun_shop_name(self) -> str:
        """
        获取店铺名

        Returns:
            str: _description_
        """
        return self.start_path.parts[1]

    @property
    def __fun_start_num(self) -> int:
        return int(self.start_path.stem)

    @staticmethod
    def __fun_get_folder_num(path_obj: Path) -> int:
        try:
            return int(path_obj.stem)
        except ValueError:
            return 0

    @property
    def __parnet_path(self) -> Path:
        return self.start_path.parent

    @property
    def fun_all_folder(self) -> list[Path]:
        """
        构建所有文件夹

        Returns:
            list[Path]: _description_
        """
        all_path = []
        for in_path in self.__parnet_path.iterdir():
            if (
                in_path.is_dir()
                and self.__fun_get_folder_num(path_obj=in_path) >= self.__fun_start_num
                and self.__fun_get_folder_num(path_obj=in_path) <= self.end_num
            ):
                all_path.append(in_path)

        all_path.sort(key=self.__fun_get_folder_num)

        return all_path

    @property
    def fun_all_folder_num(self) -> list[int]:
        """
        获取所有文件夹数字

        Returns:
            list[int]: _description_
        """
        return [self.__fun_get_folder_num(k) for k in self.fun_all_folder]
