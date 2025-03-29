"""删除指定图片."""

from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from Router.fun_文件夹操作 import fun_文件夹初始化

router = APIRouter()


class Item(BaseModel):
    image_path: str
    root_path: str


@router.post("/删除指定图片")
def fun_dele_image(item: Item) -> dict:
    """删除指定图片."""
    material_structure = fun_文件夹初始化(root_path=item.root_path)
    image_path = Path(item.image_path)
    thumb_path = image_path.with_stem(f"{image_path.stem}_thumb")
    material_path = Path(
        image_path.as_posix().replace(
            material_structure.preview_path,
            material_structure.material_path,
        ),
    )
    thumb_path.unlink()
    image_path.unlink()
    material_path.unlink()
    return {"message": "删除成功"}
