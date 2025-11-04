from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片横向拼接 import fun_图片横向拼接
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from pathlib import Path
from PIL import Image
from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob
from MaterialEdit.setting import IMAGE_SUFFIX


def fun_文件夹内图片两排拼接(image_path: Path):
    """
    遍历文件夹里面的所有图片
    然后把图片按照每行两张进行拼接
    """

    images = []
    for img_path in rglob(image_path, IMAGE_SUFFIX):
        im = Image.open(img_path)
        images.append(im)
    group_images = [images[i : i + 2] for i in range(0, len(images), 2)]
    line_images = []
    for group in group_images:
        if len(group) != 2:
            continue
        line_im = fun_图片横向拼接(group, spacing=15, bg_color=(255, 255, 255, 255))
        line_images.append(line_im)
    final_image = fun_图片竖向拼接(
        line_images, spacing=15, bg_color=(255, 255, 255, 255)
    )
    final_image.show()


if __name__ == "__main__":
    fun_文件夹内图片两排拼接(Path(r"F:\小夕素材\11000-11999\11507\11507\小夕素材(01)"))
