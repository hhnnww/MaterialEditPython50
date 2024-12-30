"""图片文件夹."""

from pathlib import Path

from fun_素材文件夹.image_file import ImageFile
from fun_素材文件夹.material_base_func import MaterialType


class ImageFolder:
    """效果图和预览图."""

    def __init__(self, path: Path) -> None:
        """图片文件夹."""
        self.path = path

    @property
    def all_image(self) -> list[ImageFile]:
        """所有图片."""
        all_image = [
            ImageFile(path=infile)
            for infile in self.path.rglob(pattern="*")
            if infile.suffix.lower() in MaterialType.image_suffix and infile.is_file()
        ]
        all_image.sort(key=lambda k: k.num)
        return all_image
