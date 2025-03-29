"""路由文件"""

from fastapi import APIRouter

from Router.router_全自动操作 import router as router_auto_action
from Router.router_删除图片 import router as router_删除图片
from Router.router_制作详情 import router as router_制作详情
from Router.router_制作首图 import router as router_制作首图
from Router.router_图片转发 import router as router_图片转发
from Router.router_文件夹操作 import router as router_文件夹操作
from Router.router_素材下载 import router as router_素材下载
from Router.router_素材合并 import router as router_素材合并
from Router.router_获取图片 import router as router_获取图片
from Router.router_获取素材信息 import router as router_获取素材信息

router = APIRouter(prefix="/v1")

router.include_router(router_获取图片)
router.include_router(router_获取素材信息)
router.include_router(router_制作详情)
router.include_router(router_文件夹操作)
router.include_router(router_制作首图)
router.include_router(router_素材合并)
router.include_router(router_auto_action)
router.include_router(router_素材下载)
router.include_router(router_图片转发)
router.include_router(router_删除图片)
