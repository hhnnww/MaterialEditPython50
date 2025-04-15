"""获取图片缩略图"""

import io
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import Response
from PIL import Image

from MaterialEdit.fun_文件夹操作.fun_单个文件制作WEB预览图 import (
    image_make_web_thumbnail,
)

router = APIRouter(prefix="/blob")


@router.get("")
def get_img(img: str):
    bytes_io = io.BytesIO()
    new_path = image_make_web_thumbnail(image_path=Path(img))

    try:
        with Image.open(fp=new_path) as im:
            if im.mode != "RGBA":
                im = im.convert(mode="RGBA")

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
    new_path = image_make_web_thumbnail(image_path=img_path_obj)

    bytes_io = io.BytesIO()
    with Image.open(fp=new_path) as im:
        if im.mode != "RGBA":
            im = im.convert(mode="RGBA")

        im.thumbnail(size=(500, 500))
        im.save(fp=bytes_io, format="png")

    return Response(content=bytes_io.getvalue(), media_type="image/png")
