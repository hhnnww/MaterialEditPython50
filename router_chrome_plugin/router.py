"""浏览器插件工具"""

from fastapi import APIRouter

from router_chrome_plugin import (
    route_制作淘宝详情,
    route_获取店铺名和素材网站,
    router_采集素材,
)

router = APIRouter(prefix="/chrome_plugin")

# 制作淘宝详情页图片列表
router.include_router(route_制作淘宝详情.router)

# 爬取素材
router.include_router(router_采集素材.router)

# 获取基本信息
router.include_router(route_获取店铺名和素材网站.router)
