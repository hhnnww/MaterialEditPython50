"""素材编辑自动操作."""

from .fun_上传产品到淘宝 import AutoUploadProductToTaobao
from .fun_上传素材到百度网盘 import AutoUploadMaterialToBaiduYun
from .fun_下载目录移动到素材目录 import DownPathMoveToMaterialPath
from .fun_窗口操作 import fun_窗口置顶, fun_获取窗口坐标
from .fun_自动生成详情 import AutoMakeProductImage
from .fun_获取百度网盘下载链接 import AutoGetBaiDuShareLink

__all__ = [
    "AutoGetBaiDuShareLink",
    "AutoMakeProductImage",
    "AutoUploadMaterialToBaiduYun",
    "AutoUploadProductToTaobao",
    "DownPathMoveToMaterialPath",
    "fun_窗口置顶",
    "fun_获取窗口坐标",
]
