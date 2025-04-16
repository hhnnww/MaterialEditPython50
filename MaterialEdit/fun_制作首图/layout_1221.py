import math

from PIL import Image

from image_action import ImageAction
from MaterialEdit.fun_制作首图.layout_1大3小_自适应 import LayoutInit


class Layout1221(LayoutInit):
    @property
    def small_width(self) -> int:
        return math.ceil((self.xq_width - (self.spacing * 2)) / 3)

    @property
    def small_height(self) -> int:
        return math.ceil((self.xq_height - (self.spacing * 3)) / 4)

    def main(self):
        # 第一张大图
        first_line = ImageAction.ImageMerge(
            image_list=[
                self._pil_list[0].resize(
                    (
                        self.small_width * 2 + self.spacing,
                        self.small_height * 2 + self.spacing,
                    ),
                    resample=Image.Resampling.LANCZOS,
                ),
                ImageAction.ImageMerge(
                    [
                        pil.resize(
                            (self.small_width, self.small_height),
                            Image.Resampling.LANCZOS,
                        )
                        for pil in self._pil_list[1:3]
                    ],
                    spacing=self.spacing,
                    align="start",
                    direction="y",
                ).main(),
            ],
            direction="x",
            spacing=self.spacing,
            align="center",
        ).main()
        # 第二行
        second_line = ImageAction.ImageMerge(
            image_list=[
                self._pil_list[3].resize(
                    (
                        self.small_width * 2 + self.spacing,
                        self.small_height * 2 + self.spacing,
                    ),
                    resample=Image.Resampling.LANCZOS,
                ),
                ImageAction.ImageMerge(
                    [
                        pil.resize(
                            (self.small_width, self.small_height),
                            Image.Resampling.LANCZOS,
                        )
                        for pil in self._pil_list[4:6]
                    ],
                    spacing=self.spacing,
                    align="start",
                    direction="y",
                ).main(),
            ],
            direction="x",
            spacing=self.spacing,
            align="start",
        ).main()

        return (
            ImageAction.ImageMerge(
                image_list=[first_line, second_line],
                direction="y",
                spacing=self.spacing,
                align="start",
            )
            .main()
            .resize((self.xq_width, self.xq_height), Image.Resampling.LANCZOS)
        )
