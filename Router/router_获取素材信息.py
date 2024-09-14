from fastapi import APIRouter
from pydantic import BaseModel

from MaterialEdit import MaterialInfo, fun_获取素材信息
from MaterialEdit.fun_文件夹操作.fun_文件夹初始化 import fun_文件夹初始化

router = APIRouter(prefix="/GetMaterialInfo")


class GetMaterialInfoModel(BaseModel):
    root_path: str
    preview_num: int
    preview_sort: bool
    shop_name: str


@router.post("", response_model=MaterialInfo)
def get_material_info(item: GetMaterialInfoModel):
    fun_文件夹初始化(item.root_path)
    return fun_获取素材信息(
        item.root_path, used_image=item.preview_num, image_sort=item.preview_sort
    )
