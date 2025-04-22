from PIL import Image


class StyleInit:
    def __init__(
        self,
        bg: Image.Image,
        title: str,
        format: str,
        material_id: str,
        format_title: str,
        shop_name: str,
    ) -> None:
        self.bg = bg
        self.title = title
        self.format = format
        self.material_id = material_id
        self.format_title = format_title
        self.shop_name = shop_name
