"""图片文件."""

import shutil
from pathlib import Path

from PIL import Image
from tomorrow3 import threads

from fun_素材文件夹.material_base_func import MaterialType
from MaterialEdit.fun_图片编辑.fun_删除图片边框.fun_删除图片边框 import fun_删除图片边框


class ImageFile:
    def __init__(self, path: Path) -> None:
        """图片文件."""
        self.path = path

    @property
    def thumbnail_path(self) -> Path:
        """图片转换到缩略图."""
        return self.path.with_stem(stem=self.path.stem + "_thumb")

    @property
    def num(self) -> int:
        """文件名中的数字."""
        return MaterialType.fun_获取文件名中的数字(self.path.stem)

    def preview_image_path(self, material_path: Path, preview_path: Path) -> Path:
        """素材图转换到预览图."""
        return Path(
            self.path.as_posix().replace(
                material_path.as_posix(),
                preview_path.as_posix(),
            ),
        )

    @threads(5)
    def fun_复制素材图到预览图(self, material_path: Path, preview_path: Path) -> None:
        """复制素材图到预览图."""
        preview_path = self.preview_image_path(
            material_path=material_path,
            preview_path=preview_path,
        )
        preview_path.parent.mkdir(parents=True, exist_ok=True)

        if preview_path.exists() is not True:
            MaterialType.log(
                f"复制素材图到预览图{self.path.as_posix()}\t->\t{preview_path.as_posix()}",
            )
            shutil.copy(self.path, preview_path)
            self.__fun_图片转换到缩略图(800)

    def __fun_图片转换到缩略图(self, max_size: int) -> None:
        """图片转换到缩略图."""
        if self.thumbnail_path.exists() is not True:
            MaterialType.log(f"生成缩略图{self.thumbnail_path.as_posix()}")

            with Image.open(self.path.as_posix()) as im:
                im.thumbnail(size=(max_size, max_size), reducing_gap=3.0)
                im.save(self.thumbnail_path.as_posix())

    def fun_图片删除边框(self) -> None:
        """删除图片边框."""
        MaterialType.log(f"删除图片边框: {self.path}")

        with Image.open(self.path.as_posix()) as im:
            pil = im.convert("RGBA") if im.mode != "RGBA" else im
            pil = fun_删除图片边框(im=pil)
            if self.path.suffix.lower() == ".png":
                pil.save(self.path.as_posix(), format="PNG")
            else:
                pil = pil.convert(mode="RGB")
                pil.save(self.path.as_posix(), format="JPEG", quality=95)
