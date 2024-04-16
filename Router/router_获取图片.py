import io

from fastapi import APIRouter
from fastapi.responses import Response
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
