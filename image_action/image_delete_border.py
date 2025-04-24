from PIL import Image


class ImageDeleteBorder:
    @staticmethod
    def fun_删除图片边框(im: Image.Image) -> Image.Image:
        """删除图片边框"""
        # 获取左上右下四个像素点的颜色
        left_color = im.getpixel((0, im.height // 2))
        top_color = im.getpixel((im.width // 2, 0))
        right_color = im.getpixel((im.width - 1, im.height // 2))
        bottom_color = im.getpixel((im.width // 2, im.height - 1))

        # 定义裁剪边框的范围
        left, top, right, bottom = 0, 0, im.width, im.height

        # 裁剪左边
        while left < im.width:
            column = [im.getpixel((left, y)) for y in range(im.height)]
            if all(pixel == left_color for pixel in column):
                left += 1
            else:
                break

        # 裁剪上边
        while top < im.height:
            row = [im.getpixel((x, top)) for x in range(im.width)]
            if all(pixel == top_color for pixel in row):
                top += 1
            else:
                break

        # 裁剪右边
        while right > left:
            column = [im.getpixel((right - 1, y)) for y in range(im.height)]
            if all(pixel == right_color for pixel in column):
                right -= 1
            else:
                break

        # 裁剪下边
        while bottom > top:
            row = [im.getpixel((x, bottom - 1)) for x in range(im.width)]
            if all(pixel == bottom_color for pixel in row):
                bottom -= 1
            else:
                break

        # 裁剪图片
        return im.crop((left, top, right, bottom))


if __name__ == "__main__":
    ImageDeleteBorder.fun_删除图片边框(
        im=Image.open(r"F:\小夕素材\11000-11999\11228\11228\小夕素材(11).png"),
    ).show()
