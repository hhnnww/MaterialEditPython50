from fastapi import APIRouter

from .fun_制作详情 import MakeProductImageRequestModel, fun_make_material_product_image

router = APIRouter(prefix="/MakeMaterialProductImage")


@router.post("")
def make_material_product_image(item: MakeProductImageRequestModel):
    fun_make_material_product_image(item)
