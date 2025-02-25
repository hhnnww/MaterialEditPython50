"""导出图片."""

from pathlib import Path

import photoshop.api as ps
import pythoncom
from win32com.client import Dispatch

from fun_素材文件夹 import material_base_func


class ExportImage:
    @staticmethod
    def fun_PSD文件导出PNG(path_list: list[Path]) -> None:
        """PSD文件导出PNG."""
        pythoncom.CoInitialize()
        app = ps.Application()
        export_options = ps.ExportOptionsSaveForWeb()
        export_options.format = ps.SaveDocumentType.PNGSave
        export_options.PNG8 = False
        export_options.quality = 100

        for path in path_list:
            material_base_func.MaterialType.log(f"导出{path.as_posix()}为PNG")
            doc = app.open(document_file_path=path.as_posix())

            # 隐藏第一个图层
            first_layer = doc.artLayers.getByIndex(index=1)
            material_base_func.MaterialType.log(f"第一个图层名字{first_layer.name}")
            if "删除" in first_layer.name and "$" in first_layer.name:
                first_layer.visible = False

            png_path = path.with_suffix(suffix=".png").as_posix()
            doc.exportDocument(
                file_path=png_path,
                exportAs=ps.ExportType.SaveForWeb,
                options=export_options,
            )
            doc.close(saving=ps.SaveOptions.DoNotSaveChanges)

        pythoncom.CoUninitialize()

    @staticmethod
    def fun_AI文件导出PNG(path_list: list[Path]) -> None:
        """AI文件导出PNG."""
        pythoncom.CoInitialize()
        app = Dispatch(dispatch="Illustrator.Application")
        for path in path_list:
            material_base_func.MaterialType.log(f"导出{path.as_posix()}为PNG")
            doc = app.Open(path.as_posix())
            radio = int(4000 / max((int(doc.Width), int(doc.Height)))) * 100
            export_options = Dispatch("Illustrator.ExportOptionsPNG24")
            export_options.HorizontalScale = radio
            export_options.VerticalScale = radio
            export_options.ArtBoardClipping = True
            png_path = path.with_suffix(suffix=".png")
            doc.Export(
                ExportFile=png_path.as_posix(),
                ExportFormat=5,
                Options=export_options,
            )
            doc.Close(2)
        pythoncom.CoUninitialize()

    @staticmethod
    def fun_打开AI文件(path_list: list[Path]) -> None:
        """打开AI文件."""
        pythoncom.CoInitialize()
        app = Dispatch(dispatch="Illustrator.Application")
        for path in path_list[:5]:
            material_base_func.MaterialType.log(f"打开AI文件{path.as_posix()}")
            app.Open(path.as_posix())
        pythoncom.CoUninitialize()

    @staticmethod
    def fun_打开PSD文件(path_list: list[Path]) -> None:
        """打开PSD文件."""
        pythoncom.CoInitialize()
        app = Dispatch(dispatch="Photoshop.Application")
        for path in path_list[:5]:
            material_base_func.MaterialType.log(f"打开PSD文件{path.as_posix()}")
            app.Open(path.as_posix())
        pythoncom.CoUninitialize()
