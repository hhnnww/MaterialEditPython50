"""获取图片缩略图"""

import io
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import Response
from PIL import Image

from MaterialEdit.fun_文件夹操作.fun_单个文件制作WEB预览图 import (
    fun_单个文件制作WEB预览图,
)

router = APIRouter(prefix="/blob")


@router.get("")
def get_img(img: str):
    """获取缩小后的图像

    Args:
        img (str): 图像地址

    Returns:
        Response | None: 返回图片内容
        如果出错
        返回None
    """
    bytes_io = io.BytesIO()
    new_path = fun_单个文件制作WEB预览图(image_path=Path(img))

    try:
        with Image.open(fp=new_path) as im:
            if im.mode != "RGBA":
                im = im.convert(mode="RGBA")

            if im.height / im.width > 2:
                im = im.crop(box=(0, 0, im.width, int(im.width * 1.9)))

            im.thumbnail(size=(500, 500))
            im.save(fp=bytes_io, format="png")

        return Response(content=bytes_io.getvalue(), media_type="image/png")

    # 如果出现错误
    except ValueError as e:
        print(img, e)
        return None


@router.get(path="/thumbnail")
def get_thumbnail(img_path: str) -> Response:
    """获取缩略图

    Args:
        img_path (str): _description_

    Returns:
        Response: _description_
    """
    img_path_obj = Path(img_path)
    new_path = fun_单个文件制作WEB预览图(image_path=img_path_obj)

    bytes_io = io.BytesIO()
    with Image.open(fp=new_path) as im:
        if im.mode != "RGBA":
            im = im.convert(mode="RGBA")

        if im.height / im.width > 2:
            im = im.crop(box=(0, 0, im.width, int(im.width * 1.9)))

        im.thumbnail(size=(500, 500))
        im.save(fp=bytes_io, format="png")

    return Response(content=bytes_io.getvalue(), media_type="image/png")
