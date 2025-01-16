"""返回店铺列表和素材网站列表."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ShopNameModel(BaseModel):
    """获取店铺名列表和素材网站列表请求模型"""

    shop_name_list: list[str]
    material_site_list: list[str]


@router.get("/get_shop_name_material_site")
def fun_get_shop_name_material_site() -> ShopNameModel:
    """获取店铺名列表和素材网站的函数"""
    return ShopNameModel(
        shop_name_list=["小夕素材", "饭桶设计", "泡泡素材", "松子素材"],
        material_site_list=[
            "freepik",
            "千图",
            "包图",
            "摄图",
            "享设计",
            "千库",
            "青青草素材王国",
            "加油鸭素材铺",
            "漫语摄影",
            "三老爹",
            "T500",
            "猪大叔",
            "唐峰",
            "芒果",
            "巴扎嘿",
            "轨迹",
        ],
    )
