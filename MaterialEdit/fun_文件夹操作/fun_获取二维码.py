from pathlib import Path

from PIL import Image


def fun_获取二维码(shop_name: str) -> Image.Image:
    im_path = Path(__file__).parent / "files" / f"二维码-{shop_name}.png"
    im = Image.open(im_path.as_posix())
    im.thumbnail((120, 120))
    return im
