"""根目录."""

from pathlib import Path

from fun_素材文件夹.image_folder import ImageFolder
from fun_素材文件夹.material_base_func import MaterialType
from fun_素材文件夹.material_folder import MaterialFolder


class RootFolder:
    def __init__(self, path: str) -> None:
        """根目录."""
        self.root_path = Path(path)
        self.fun_验证路径()
        self.fun_初始化()

    def fun_验证路径(self) -> None:
        """验证rootpath是否正确."""
        msg = ""

        if "-" in self.root_path.stem:
            msg = "路径不能包含 -"

        root_path_depen = 3
        if len(self.root_path.parts) <= root_path_depen:
            msg = "路径深度不够"

        if self.root_path.stem == self.root_path.parent.stem:
            msg = "路径不能和父路径同名"

        if self.root_path.is_absolute() is not True:
            msg = "必须使用绝对路径，不能使用相对路径"

        if msg != "":
            raise IndexError(msg)

    def fun_初始化(self) -> None:
        """传入root_path时初始化文件夹."""
        if self.mateiral_path.path.exists() is not True:
            self.mateiral_path.path.mkdir()

        for inpath in self.root_path.iterdir():
            if inpath.is_file() or (
                inpath.is_dir()
                and inpath
                not in [
                    self.mateiral_path.path,
                    self.preview_path.path,
                    self.effect_path.path,
                    self.design_path.path,
                ]
            ):
                MaterialType.log(f"移动到素材目录{inpath}")
                inpath.rename(self.mateiral_path.path / inpath.name)

    max_open_file = 5

    @property
    def mateiral_path(self) -> MaterialFolder:
        """素材路径."""
        return MaterialFolder(self.root_path / self.root_path.stem)

    @property
    def preview_path(self) -> ImageFolder:
        """预览图路径."""
        return ImageFolder(self.root_path / "预览图")

    @property
    def design_path(self) -> ImageFolder:
        """设计图路径."""
        return ImageFolder(self.root_path / "设计图")

    @property
    def effect_path(self) -> ImageFolder:
        """效果图路径."""
        return ImageFolder(self.root_path / "效果图")
