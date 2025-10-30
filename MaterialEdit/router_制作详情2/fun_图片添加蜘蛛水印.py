from PIL import Image

from pathlib import Path


def fun_详情图片添加蜘蛛水印(im: Image.Image) -> Image.Image:
    """详情图片添加蜘蛛水印

    Args:
        im (Image.Image): 详情图片

    Returns:
        Image.Image: 添加蜘蛛水印后的图片
    """
    watermark = Image.open(Path(__file__).parent / "zhizhu.png")
    watermark.thumbnail((int(im.width * 1), 999999), Image.Resampling.LANCZOS)
    left = im.width // 2 - watermark.width // 2
    top = 0

    for x in range(0, im.width, watermark.width):
        for y in range(0, im.height, watermark.height):
            im.paste(watermark, (left, top), watermark)
            top += watermark.height + 300

    return im
