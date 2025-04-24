import math
from itertools import cycle

from PIL import Image

from image_action.image_action import ImageAction
from MaterialEdit.fun_制作首图.class_layout_init import LayoutInit
from MaterialEdit.type import ImageModel


class LayoutTransparentElementsArrangement(LayoutInit):
    @property
    def fun_计算行高(self) -> int:
        """计算行高"""
        return math.floor((self.xq_height - ((self.col + 1) * self.spacing)) / self.col)

    def fun_处理单个图片(self, im: Image.Image) -> Image.Image:
        """处理单个图片"""
        im.thumbnail((self.fun_计算行高, 999999), Image.Resampling.LANCZOS)
        return ImageAction.fun_删除图片边框(im)

    def main(self) -> Image.Image:
        """主函数"""
        line = []
        rows = []
        for image in cycle(self.image_list):
            im = self.fun_处理单个图片(self._fun_打开图片(image.path))
            line.append(im)
            if (
                sum([im.width for im in line]) + ((len(line) - 1) * self.spacing)
                >= self.xq_width
            ):
                rows.append(ImageAction.fun_图片横向拼接(line, self.spacing, "center"))
                line = []

            if len(rows) >= self.col:
                break

        bg = ImageAction.fun_图片竖向拼接(rows, self.spacing, "center")
        bg = bg.crop(
            (
                (bg.width - self.xq_width) // 2,
                0,
                self.xq_width + ((bg.width - self.xq_width) // 2),
                self.xq_height,
            ),
        )
        self.fun_储存design_image(bg)
        return bg.resize(
            (self.xq_width, self.xq_height),
            Image.Resampling.LANCZOS,
        )


if __name__ == "__main__":
    from pathlib import Path

    image_list = [
        ImageModel(
            path=infile.as_posix(),
        )
        for infile in Path(r"F:\小夕素材\11000-11999\11254\11254").iterdir()
        if infile.suffix.lower() in [".png"] and infile.is_file()
    ]
    LayoutTransparentElementsArrangement(
        image_list=image_list,
        xq_width=1500,
        xq_height=1300,
        col=4,
        spacing=10,
        out_space=False,
        crop_position="center",
        bg_color=(255, 255, 255, 255),
        radio=False,
        design_path="",
    ).main().show()
