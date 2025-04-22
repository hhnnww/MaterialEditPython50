"""素材文件夹中的子文件夹."""

from pathlib import Path

from fun_素材文件夹.material_base_func import MaterialType


class MaterialSubFolder:
    def __init__(self, path: Path) -> None:
        """素材文件夹内的子目录."""
        self.path = path

    @property
    def file_num(self) -> int:
        """获取文件名中的数字."""
        return MaterialType.fun_获取文件名中的数字(stem=self.path.stem)

    def fun_子目录文件移动到根目录(self) -> None:
        """子目录所有文件移动到根目录."""
        MaterialType.fun_移动到根目录(folder=self.path)

    def fun_子目录重命名(self, new_stem: str) -> None:
        """子目录重命名."""
        self.path.rename(self.path.with_stem(new_stem))

    def fun_子目录AI重命名(self) -> None:
        """子目录的AI文件重命名."""
        for num, infile in enumerate(
            [
                infile
                for infile in self.path.iterdir()
                if infile.suffix.lower() in [".ai", ".eps"] and infile.is_file()
            ],
        ):
            new_stem = (
                f"{self.path.stem}" if num == 0 else f"{self.path.stem}_{num + 1}"
            )
            infile.rename(infile.with_stem(new_stem))

    def fun_AI文件夹重构(self) -> None:
        """把ai文件的链接文件移动到LINKS目录.

        构建所有非AI EPS的文件列表
        如果列表不为空, 创建LINKS目录
        移动文件到LINKS目录
        """
        move_file_list = [
            infile
            for infile in self.path.rglob("*")
            if infile.suffix.lower() not in [".ai", ".eps"] and infile.is_file()
        ]

        link_path = self.path / "Links"
        if len(move_file_list) > 0:
            link_path.mkdir()

        for infile in move_file_list:
            MaterialType.log(msg=f"AI文件夹重构{self.path.as_posix()}")
            new_path = link_path / infile.name
            infile.rename(new_path)
