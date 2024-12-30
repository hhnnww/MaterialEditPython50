"""导出PNG图片."""

from typing import ClassVar

import photoshop.api as ps

from fun_素材文件夹.fun_PS文件处理.ps_base import PhotoShopBase


class PhotoShopExportPng(PhotoShopBase):
    first_layer_ad_name: ClassVar[list[str]] = ["删除", "$", "SY"]

    def _fun_隐藏第一个图层(self) -> None:
        """隐藏第一个图层."""
        for ad_name in self.first_layer_ad_name:
            if ad_name in self.fun_所有图层[0].name:
                self.fun_所有图层[0].visible = False

    def main(self) -> None:
        """导出图片."""
        self._fun_隐藏第一个图层()
        self.fun_导出PNG()
        self.doc.close(saving=ps.SaveOptions.DoNotSaveChanges)
