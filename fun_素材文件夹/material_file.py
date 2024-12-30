"""素材文件."""

from pathlib import Path

from fun_素材文件夹.image_file import ImageFile
from fun_素材文件夹.material_base_func import MaterialType


class MaterialFile:
    """单个素材文件."""

    def __init__(self, path: Path) -> None:
        """素材文件."""
        self.path = path

    @property
    def format(self) -> str:
        """素材格式大写."""
        return self.path.suffix.upper().replace(".", "")

    @property
    def material_images(self) -> list[ImageFile]:
        """单个素材文件对应的素材图."""
        return [
            ImageFile(path=infile)
            for infile in self.path.parent.iterdir()
            if infile.suffix in MaterialType.image_suffix and infile.is_file() and self.path.stem in infile.name
        ]

    @property
    def has_material_image(self) -> bool:
        """判断是否有预览图."""
        return len(self.material_images) != 0

    @property
    def num(self) -> int:
        """获取文件名中的数字."""
        return MaterialType.fun_获取文件名中的数字(self.path.stem)

    def fun_修改素材源文件以及素材图和预览图名称(self, new_stem: str, material_path: Path, preview_path: Path) -> None:
        """素材文件和对应的素材图以及预览图重命名."""
        for image in self.material_images:
            image.path.rename(image.path.with_stem(new_stem))
            preview_path = image.preview_image_path(material_path=material_path, preview_path=preview_path)
            if preview_path.exists() is True:
                preview_path.rename(preview_path.with_stem(new_stem))

        self.path.rename(self.path.with_stem(new_stem))

    def fun_修改素材源文件对应的素材图名称(self, material_path: Path, preview_path: Path) -> None:
        """素材文件对应的素材图重命名.

        AI到处的多画板图片和PS导出的多文件图片
        """
        for num, image in enumerate(self.material_images):
            MaterialType.log(f"图片重命名{image.path.as_posix()}")
            new_stem = f"{self.path.stem}" if num == 0 else f"{self.path.stem}_{num}"
            # 修改素材图
            image.path.rename(image.path.with_stem(new_stem))
            # 修改预览图
            preview_image = image.preview_image_path(material_path=material_path, preview_path=preview_path)
            if preview_image.exists() is True:
                preview_image.rename(preview_image.with_stem(new_stem))

    def fun_移动到子目录(self, material_path: Path, preview_path: Path) -> None:
        """移动到子目录.

        把AI文件和PSD文件以及对应的素材图移动到子目录里面
        """
        if self.path.parent == material_path:
            parent_path = material_path / f"{self.path.stem}"
            parent_path.mkdir()
            # 素材源文件移动到子目录
            self.path.rename(parent_path / self.path.name)

            # 素材图和预览图移动到子目录
            for image in self.material_images:
                # 素材图移动到子目录
                image.path.rename(parent_path / image.path.name)

                # 预览图移动到子目录
                preview_image = image.preview_image_path(material_path=material_path, preview_path=preview_path)
                if preview_image.exists() is True:
                    # 创建父文件夹
                    parent_path = preview_image.parent / f"{self.path.stem}"
                    parent_path.mkdir()
                    preview_image.rename(parent_path / preview_image.name)

                    # 缩略图移动
                    thumbnail_image = ImageFile(path=preview_image).thumbnail_path
                    if thumbnail_image.exists() is True:
                        thumbnail_image.rename(parent_path / thumbnail_image.name)
