from pathlib import Path

from win32com.client import Dispatch


def com_psd导出png(
    ref_doc,
    file: Path,
    ad_layer_name: str,
    del_ad_layer: bool = False,
) -> Path:
    png_path = file.with_suffix(".jpg")

    if ref_doc.ArtLayers.Count > 0:
        # 第一个广告图层
        ad_layer = ref_doc.ArtLayers.Item(1)

        if ad_layer.Name in [
            ad_layer_name,
            "隐藏 或 删除此图层即可开始您的编辑.",
            "隐藏 或 删除此图层即可开始您的编辑.",
            "二维码",
        ]:
            if del_ad_layer is True:
                ad_layer.AllLocked = False
                ad_layer.Delete()
            else:
                ad_layer.Visible = False

    options = Dispatch("Photoshop.ExportOptionsSaveForWeb")
    options.Format = 6
    options.Quality = 60
    ref_doc.Export(png_path.as_posix(), 2, options)

    if ref_doc.ArtLayers.Count > 0:
        ad_layer = ref_doc.ArtLayers.Item(1)
        if del_ad_layer is False and ad_layer.Name == ad_layer_name:
            ad_layer.Visible = True

    return png_path
