"""画册素材的图片添加阴影."""

import math
from pathlib import Path

from PIL import Image
from tomorrow3 import threads
from tqdm import tqdm

from MaterialEdit.setting import IMAGE_SUFFIX


@threads(5)
class PhotoAddShadow:
    """单个图片添加阴影."""

    def __init__(self, image: Path, col: int, shadow_pil: Image.Image) -> None:
        """输入单个图片."""
        self.image = image
        self.col = col
        self.shadow_pil = shadow_pil

    @property
    def can_edit(self) -> bool:
        """图片是否可以编辑.

        如果是缩略图就不编辑.
        """
        return "thumb" not in self.image.stem

    @property
    def im(self) -> Image.Image:
        """打开预览图."""
        im = Image.open(self.image)
        if im.mode.lower() != "rgba":
            im = im.convert("RGBA")
        return im

    @property
    def left_position_list(self) -> list[int]:
        """构建左边起始点的坐标列表.

        根据列表长度来乘以单个列表宽度没有设置起始点.
        """
        left_position_list: list[int] = []
        single_col_width = math.ceil(self.im.width / self.col)

        while len(left_position_list) < self.col:
            left_position_list.append((len(left_position_list)) * single_col_width)

        return left_position_list

    def main(self) -> None:
        """单个图片开始添加阴影."""
        if self.can_edit is not True:
            return

        im = self.im
        shadow_pil = self.shadow_pil

        shadow_pil.thumbnail(
            size=(int(im.width / self.col / 2), 999999),
            resample=Image.Resampling.LANCZOS,
            reducing_gap=3,
        )
        _r, _g, _b, a = shadow_pil.split()
        for left in self.left_position_list:
            top = 0
            while top < self.im.height:
                im.paste(im=shadow_pil, box=(left, top), mask=a)
                top += shadow_pil.height

        if self.image.suffix.lower() != ".png":
            im = im.convert("RGB")

        im.save(self.image.as_posix())


class PreviewImagePhotoAddShadow:
    """如果是画册素材.

    预览图文件夹所有图片添加阴影.
    """

    def __init__(self, preview_path_str: str, col: int) -> None:
        """输入预览图文件夹."""
        self.preview_path = Path(preview_path_str)
        self.col = col

    @property
    def all_image(self) -> list[Path]:
        """构建所有图片列表."""
        return [
            image
            for image in self.preview_path.rglob("*")
            if image.is_file() and image.suffix.lower() in IMAGE_SUFFIX
        ]

    @property
    def shadow_pil(self) -> Image.Image:
        """阴影图片."""
        return Image.open(Path(__file__).parent / "files" / "折页阴影.png")

    def main(self) -> None:
        """开始添加阴影."""
        for image in tqdm(iterable=self.all_image, desc="图片添加阴影", ncols=100):
            PhotoAddShadow(image=image, col=self.col, shadow_pil=self.shadow_pil).main()


if __name__ == "__main__":
    PreviewImagePhotoAddShadow(
        preview_path_str=r"F:\小夕素材\10000-20000\10961\10961",
        col=2,
    ).main()
