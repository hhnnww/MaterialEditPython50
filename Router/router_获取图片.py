import io
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse, Response
from MaterialEdit.fun_文件夹操作.fun_单个文件制作WEB预览图 import (
    fun_单个文件制作WEB预览图,
)
from PIL import Image

router = APIRouter(prefix="/blob")


@router.get("")
def get_img(img: str):
    bytes_io = io.BytesIO()

    try:
        with Image.open(img) as im:
            if im.mode != "RGBA":
                im = im.convert("RGBA")

            if im.height / im.width > 2:
                im = im.crop((0, 0, im.width, int(im.width * 1.9)))

            im.thumbnail((500, 500))
            im.save(bytes_io, format="png")

        return Response(bytes_io.getvalue(), media_type="image/png")

    # 如果出现错误
    except ValueError as e:
        print(img, e)
        return None


@router.get("/thumbnail")
def get_thumbnail(img_path: str):
    img_path_obj = Path(img_path)
    new_path = fun_单个文件制作WEB预览图(image_path=img_path_obj)
    return FileResponse(path=new_path)
