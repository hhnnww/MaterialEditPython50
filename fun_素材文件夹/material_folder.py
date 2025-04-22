"""素材文件夹."""

from pathlib import Path

from fun_素材文件夹.image_file import ImageFile
from fun_素材文件夹.material_base_func import MaterialType
from fun_素材文件夹.material_file import MaterialFile
from fun_素材文件夹.material_sub_folder import MaterialSubFolder


class MaterialFolder:
    def __init__(self, path: Path) -> None:
        """素材目录."""
        self.path = path

    @property
    def all_material(self) -> list[MaterialFile]:
        """获取所有素材."""
        all_material = [
            MaterialFile(path=infile)
            for infile in self.path.rglob(pattern="*")
            if infile.suffix.lower() in MaterialType.material_suffix
            and infile.is_file()
        ]
        all_material.sort(key=lambda k: k.num)
        return all_material

    @property
    def all_sub_path(self) -> list[MaterialSubFolder]:
        """所有子目录."""
        all_sub_path = [
            MaterialSubFolder(infile)
            for infile in self.path.iterdir()
            if infile.is_dir()
        ]
        all_sub_path.sort(key=lambda k: k.file_num)
        return all_sub_path

    @property
    def all_image(self) -> list[ImageFile]:
        """所有图片."""
        return [
            ImageFile(path=infile)
            for infile in self.path.rglob(pattern="*")
            if infile.suffix.lower() in MaterialType.image_suffix and infile.is_file()
        ]
