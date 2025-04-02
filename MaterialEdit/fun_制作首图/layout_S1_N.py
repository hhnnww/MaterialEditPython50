"""布局函数layout_s1_n

此函数用于根据给定的图片列表和布局参数生成一个包含大图和小图的组合图像。
参数:
    image_list (list[ImageModel]): 包含图片路径和相关信息的 ImageModel 对象列表。
    xq_width (int): 输出图像的宽度。
    xq_height (int): 输出图像的高度。
    spacing (int): 图片之间的间距。
    col (int): 小图的列数。
返回:
    Image.Image: 生成的组合图像。
功能描述:
1. 计算大图和小图的尺寸。
2. 将第一张图片裁剪为大图，并添加边框和圆角如果 spacing > 0
3. 将大图粘贴到背景图像的左上角。
4. 遍历剩余图片，将其裁剪为小图，并添加边框和圆角 如果 spacing > 0
5. 将小图按列数和间距依次粘贴到背景图像中。
6. 最多处理 col * 2 + 1 张小图。
注意:
- 图片裁剪、添加边框和圆角的功能由外部函数实现。
- 如果图片数量不足，可能会导致部分区域为空。
"""

from PIL import Image
from tqdm import tqdm

from MaterialEdit.fun_图片编辑.fun_图片切换到圆角 import fun_图片切换到圆角
from MaterialEdit.fun_图片编辑.fun_图片画边框 import fun_图片画边框
from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_图片裁剪 import fun_图片裁剪
from MaterialEdit.type import ImageModel


def layout_s1_n(
    image_list: list[ImageModel],
    xq_width: int,
    xq_height: int,
    spacing: int,
    col: int,
) -> Image.Image:
    """布局函数，用于生成首图布局。

    此函数接收一组图片，并根据指定的宽度、高度、间距和列数，生成一个包含大图和小图的布局图像。
    参数:
        image_list (list[ImageModel]): 包含图片路径的 ImageModel 对象列表
        第一张图片为大图，其余为小图。
        xq_width (int): 布局图像的总宽度。
        xq_height (int): 布局图像的总高度。
        spacing (int): 图片之间的间距。
        col (int): 小图的列数。
    返回:
        Image.Image: 生成的布局图像。
    注意:
        - 第一张图片会被裁剪为大图并放置在布局的左上角。
        - 其余图片会被裁剪为小图并排列在大图右侧和下方。
        - 如果间距大于 0 会为图片添加边框和圆角效果。
        - 最多排列 col * 2 + 1 张小图，多余的图片会被忽略。
    """
    single_col = (xq_width - ((col + 3) * spacing)) / (col + 2)
    large_image_width = ((single_col * 2) + spacing) * 0.9
    large_image_height = xq_height - (spacing * 2)
    large_im = Image.open(image_list[0].path)
    large_im = fun_图片裁剪(
        large_im,
        int(large_image_width),
        int(large_image_height),
        position="center",
    )

    small_im_height = (xq_height - (spacing * 3)) / 2

    left, top = spacing, spacing
    bg = Image.new("RGBA", (xq_width, xq_height), (255, 255, 255, 255))
    if spacing > 0:
        large_im = fun_图片画边框(large_im, (240, 240, 240, 255))
        large_im = fun_图片切换到圆角(large_im, 15, (255, 255, 255, 255))
    bg.paste(large_im, (left, top))

    left = left + large_im.width + spacing

    small_width = (xq_width - large_image_width - (spacing * (col + 2))) / col

    for num, small_im in enumerate(
        tqdm(image_list[1:], ncols=100, desc="制作首图"),
        start=1,
    ):
        im = Image.open(small_im.path)
        im = fun_图片裁剪(
            im,
            width=int(small_width),
            height=int(small_im_height),
            position="center",
        )
        if spacing > 0:
            im = fun_图片画边框(im, (240, 240, 240, 255))
            im = fun_图片切换到圆角(im, 15, (255, 255, 255, 255))
        bg.paste(im, (int(left), top))
        left = left + im.width + spacing

        if left >= bg.width - spacing - 5:
            left = large_image_width + int(spacing * 2)
            top += im.height + spacing

        if num == col * 2 + 1:
            break

    return bg
