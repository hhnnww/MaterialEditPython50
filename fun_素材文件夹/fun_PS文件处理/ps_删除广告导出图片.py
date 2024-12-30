"""删除广告导出PNG图片."""

from typing import ClassVar

import photoshop.api as ps

from fun_素材文件夹.fun_PS文件处理.ps_base import PhotoShopBase


class PhotoShopDeleAdExportPng(PhotoShopBase):
    ad_layer_name_list: ClassVar[list[str]] = ["$", "SY"]

    def fun_遍历图层删除广告(self) -> None:
        """遍历图层 删除包含广告名字的图层."""
        for layer in self.fun_所有图层:
            for ad_layer_name in self.ad_layer_name_list:
                if ad_layer_name in layer.name:
                    layer.delete()

    def main(self) -> None:
        """遍历图层 删除广告 导出PNG."""
        self.fun_遍历图层删除广告()
        self.fun_导出PNG()
        self.doc.close(saving=ps.SaveOptions.DoNotSaveChanges)
