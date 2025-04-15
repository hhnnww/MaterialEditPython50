"""删除psd文件中的图片名称"""

import contextlib
from pathlib import Path

import yaml
from win32com.client import CDispatch, Dispatch

from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob
from MaterialEdit.setting import IMAGE_SUFFIX


class DeleteImageName:
    def __init__(self, material_path: Path, shop_name: str) -> None:
        """Initialize the class with material path and shop name."""
        self.material_path = material_path
        self.app = Dispatch("Photoshop.Application")
        self.shop_name = shop_name

    @property
    def __ad_name_list(self) -> dict[str, list[str]]:
        """获取广告名称列表"""
        ad_name_yaml = Path(__file__).parent / "ad_name_list.yaml"
        with ad_name_yaml.open(encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    @property
    def __replace_text_list(self) -> dict:
        """本文替换列表"""
        text_replace_yaml = Path(__file__).parent / "replace_text_list.yaml"
        with text_replace_yaml.open(encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    @property
    def all_image(self) -> list[Path]:
        """获取所有图片文件"""
        return [
            infile
            for infile in self.material_path.rglob("*")
            if infile.is_file() and infile.suffix.lower() in IMAGE_SUFFIX
        ]

    @property
    def all_psd(self) -> list[Path]:
        """获取所有psd文件"""
        all_psd = rglob(self.material_path.as_posix(), suffix=[".psd", ".psb"])

        return [
            infile
            for infile in all_psd
            if infile.stem not in [image.stem for image in self.all_image]
        ]

    def fun_递归遍历当前PSD所有图层(self, doc: CDispatch) -> list[CDispatch]:
        """递归遍历当前PSD所有图层"""
        layers = []
        for layer in doc.Layers:
            if layer.typename == "LayerSet":
                layer.Name = f"编组 {layer.ID}"
                layers += self.fun_递归遍历当前PSD所有图层(layer)
            else:
                layers.append(layer)
        return layers

    def __fun_导入广告(self, doc: CDispatch) -> None:
        tb_ad_png = (
            Path(__file__).parent.parent
            / "fun_PS文件处理"
            / "img"
            / self.shop_name
            / "二维码.png"
        )
        if (
            doc.ArtLayers.Count > 0
            and doc.ArtLayers.Item(1).Name == self.__ad_name_list["first_name"]
        ):
            doc.ArtLayers.Item(1).Visible = True
            return

        doc.ArtLayers.Add()
        desc = Dispatch("Photoshop.ActionDescriptor")
        desc.PutPath(self.app.CharIDToTypeID("null"), tb_ad_png)
        self.app.ExecuteAction(self.app.CharIDToTypeID("Plc "), desc)

        if doc.ArtLayers.Count > 0:
            doc.ArtLayers.Item(1).Name = self.__ad_name_list["first_name"]

    def __fun_广告图层处理(self, layer: CDispatch) -> None:
        """获取广告图层"""
        if layer.Name.lower() in [
            ad_name.lower() for ad_name in self.__ad_name_list.get("ad_name_list", [])
        ]:
            layer.AllLocked = False
            layer.Visible = False
            layer.Delete()

    def __fun_文字图层处理(self, layer: CDispatch) -> None:
        """获取文字图层"""
        replace_name_list = self.__replace_text_list.get("replace_name_list", [])
        text = layer.TextItem.Contents.lower()

        replace_state = False
        for rep_name in replace_name_list:
            if rep_name[0] in text.lower():
                text = text.replace(rep_name[0], rep_name[1])
                replace_state = True

        if replace_state is True:
            layer.TextItem.Font = "IBMPlexSansSC"
            layer.TextItem.Contents = text

        layer.Name = text

    def __fun_处理单个PSD文件(self, psd_path: Path) -> None:
        """编辑单个psd文件"""
        state = False
        with contextlib.suppress(Exception):
            doc = self.app.Open(psd_path.as_posix())
            state = True

        psd_error_size = 4000
        if state is False and psd_path.stat().st_size == psd_error_size:
            psd_path.unlink()
            return

        text_layer_kind = 2
        for layer in self.fun_递归遍历当前PSD所有图层(doc):
            if layer.Kind != text_layer_kind:
                self.__fun_广告图层处理(layer)
            else:
                self.__fun_文字图层处理(layer)
        self.__fun_导出PSD文档为PNG(doc, png_path=psd_path.with_suffix(".png"))
        self.__fun_导入广告(doc)
        doc.Save()
        doc.Close(2)

    def __fun_导出PSD文档为PNG(self, doc: CDispatch, png_path: Path) -> None:
        """导出png文件"""
        export_option = Dispatch("Photoshop.ExportOptionsSaveForWeb")
        export_option.Format = 13
        export_option.PNG8 = False
        export_option.Dither = 2
        doc.Export(png_path.as_posix(), 2, export_option)

    def main(self) -> None:
        """删除psd文件中的图片名称"""
        for psd_path in self.all_psd:
            self.__fun_处理单个PSD文件(psd_path)


if __name__ == "__main__":
    material_path = Path(r"F:\小夕素材\11000-11999\11226\11226")
    delete_image_name = DeleteImageName(
        material_path=material_path,
        shop_name="小夕素材",
    )
    delete_image_name.main()
