"""把两个素材文件夹合并到一起"""

from fastapi import APIRouter
from pydantic import BaseModel

from MaterialEdit import fun_素材文件夹合并

router = APIRouter(prefix="/MaterialMerge")


class MaterialMergeModel(BaseModel):
    """素材合并模型

    Args:
        BaseModel (_type_): _description_
    """

    shop_name: str
    ori_path: str
    dst_path: str


@router.post(path="")
def material_merge(item: MaterialMergeModel) -> None:
    """素材合并函数

    Args:
        item (MaterialMergeModel): _description_
    """
    fun_素材文件夹合并(
        ori_path=item.ori_path, dst_path=item.dst_path, shop_name=item.shop_name
    )
