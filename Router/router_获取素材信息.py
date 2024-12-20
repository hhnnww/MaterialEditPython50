from fastapi import APIRouter
from pydantic import BaseModel

from MaterialEdit import MaterialInfo, fun_获取素材信息
from MaterialEdit.fun_文件夹操作.fun_文件夹初始化 import fun_文件夹初始化

router = APIRouter(prefix="/GetMaterialInfo")


class GetMaterialInfoModel(BaseModel):
    """获取素材信息模型."""

    root_path: str
    preview_num: int
    preview_sort: bool
    shop_name: str


@router.post(path="")
def get_material_info(item: GetMaterialInfoModel) -> MaterialInfo:
    """获取素材信息路由."""
    fun_文件夹初始化(root_path=item.root_path)
    return fun_获取素材信息(
        root_path=item.root_path,
        used_image=item.preview_num,
        image_sort=item.preview_sort,
    )
