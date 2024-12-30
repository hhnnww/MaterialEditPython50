"""递归遍历所有的图层 删除包含广告名字的图层."""

from __future__ import annotations

from typing import TYPE_CHECKING

import photoshop.api as ps

if TYPE_CHECKING:
    from pathlib import Path

    from photoshop.api._artlayer import ArtLayer
    from photoshop.api._document import Document
    from photoshop.api._layerSet import LayerSet


class PhotoShopBase:
    def __init__(self, path: Path) -> None:
        """PSD文件路径."""
        self.path = path
        self.png_path = path.with_suffix(".png")

        self.app = ps.Application()
        self.doc = self.app.open(document_file_path=self.path.as_posix())

    @staticmethod
    def __fun_递归图层编组(in_object: LayerSet | Document) -> list[LayerSet | Document]:
        """递归遍历图层."""
        in_layer_list = [in_object]
        for in_layer in in_object.layerSets:
            in_layer_list.extend(PhotoShopBase.__fun_递归图层编组(in_layer))
        return in_layer_list

    @property
    def fun_所有图层编组(self) -> list[LayerSet | Document]:
        """所有图层编组."""
        return self.__fun_递归图层编组(self.doc)

    @property
    def fun_所有图层(self) -> list[ArtLayer]:
        """所有图层."""
        all_layer = []
        for layer in self.fun_所有图层编组:
            all_layer.extend(list(layer.artLayers))
        return all_layer

    def fun_导出PNG(self) -> None:
        """导出PNG."""
        export_options = ps.ExportOptionsSaveForWeb()
        export_options.format = ps.SaveDocumentType.PNGSave
        export_options.PNG8 = False
        export_options.quality = 100

        self.doc.Export(
            file_path=self.png_path.as_posix(),
            exportAs=ps.ExportType.SaveForWeb,
            options=export_options,
        )
