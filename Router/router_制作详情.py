from fastapi import APIRouter

from MaterialEdit.router_制作详情2.fun_制作详情2 import (
    MakeProductImageRequestModel,
    fun_制作详情2,
)

router = APIRouter(prefix="/MakeMaterialProductImage")


@router.post("")
def make_material_product_image(item: MakeProductImageRequestModel):
    fun_制作详情2(item)
