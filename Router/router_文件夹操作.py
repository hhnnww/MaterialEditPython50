from fastapi import APIRouter

from Router.fun_文件夹操作 import (
    RequestMaterialPathActionModel,
    fun_material_path_action,
)

router = APIRouter(prefix="/MaterialPathAction")


@router.post("")
def material_path_action(item: RequestMaterialPathActionModel) -> None:
    """文件夹操作"""
    fun_material_path_action(item)
