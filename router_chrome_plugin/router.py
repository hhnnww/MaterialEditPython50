"""浏览器插件工具"""

from fastapi import APIRouter

from router_chrome_plugin import router_get_base_info, router_make_tb_xq_image_list, router_scrapy_material

router = APIRouter(prefix="/chrome_plugin")

# 制作淘宝详情页图片列表
router.include_router(router_make_tb_xq_image_list.router)

# 爬取素材
router.include_router(router_scrapy_material.router)

# 获取基本信息
router.include_router(router_get_base_info.router)
