from PIL import Image

from MaterialEdit.type import ImageModel


class LayoutInit:
    def __init__(
        self,
        image_list: list[ImageModel],
        xq_width: int,
        xq_height: int,
        spacing: int,
        col: int,
    ) -> None:
        self.image_list = image_list
        self.xq_width = xq_width
        self.xq_height = xq_height
        self.spacing = spacing
        self.col = col

    @property
    def pil_list(self) -> list[Image.Image]:
        pil_list = []
        for image in self.image_list:
            im = Image.open(image.path)
            if im.mode.lower() != "rgba":
                im = im.convert("RGBA")

            pil_list.append(im)

        return pil_list
