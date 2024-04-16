from fastapi import APIRouter
from pydantic import BaseModel

from MaterialEdit import fun_素材文件夹合并

router = APIRouter(prefix="/MaterialMerge")


class MaterialMergeModel(BaseModel):
    shop_name: str
    ori_path: str
    dst_path: str


@router.post("")
def material_merge(item: MaterialMergeModel):
    fun_素材文件夹合并(ori_path=item.ori_path, dst_path=item.dst_path, shop_name=item.shop_name)
