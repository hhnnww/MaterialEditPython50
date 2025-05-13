"""处理psd文件."""

from __future__ import annotations

import time
from pathlib import Path
from uuid import uuid1

from passlib.context import CryptContext
from win32com.client import CDispatch, Dispatch

from MaterialEdit.fun_PS文件处理.fun_对比所有导出的图片 import (
    fun_打开图片,
    run_对比所有图片,
)
from MaterialEdit.fun_PS文件处理.fun_导出PNG import com_psd导出png
from MaterialEdit.fun_PS文件处理.fun_导出图层PNG import run_导出所有图层
from MaterialEdit.fun_PS文件处理.fun_插入广告 import fun_插入广告
from MaterialEdit.fun_PS文件处理.fun_文字图层替换广告 import com_文字图层广告
from MaterialEdit.fun_PS文件处理.fun_普通图层替换广告 import com_普通图层广告
from MaterialEdit.fun_PS文件处理.fun_清理注释 import fun_清理注释
from MaterialEdit.fun_PS文件处理.model import (
    IncludeName,
    IsName,
    TextReplaceName,
    database,
)


class LayerType:
    ArtLayer = 1
    LayerSet = 2


class ArtLayerKind:
    TextLayer = 2


class PSFile:
    def __init__(
        self,
        ps_path: str,
        tb_name: str,
        ad_pic_list: list[Path],
    ) -> None:
        """输入psd文件地址 店铺名 广告关键词列表."""
        self.ps_path = ps_path
        self.tb_name = tb_name

        self.app = Dispatch("photoshop.application")
        self.app.displayDialogs = 3

        self.app.Open(ps_path)
        self.doc = self.app.ActiveDocument

        self.ad_layer_name = "隐藏 或 删除此图层即可开始您的编辑."
        self.ad_pic_list = ad_pic_list
        self.pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

        fun_清理注释(self.app)

    @staticmethod
    def get_all_layer(in_object: CDispatch) -> list:
        """获取所有图层."""
        in_layer_list = []
        for in_layer in in_object.layers:
            visible = in_layer.Visible
            if in_layer.AllLocked is True:
                in_layer.AllLocked = False
                in_layer.Visible = visible

            if in_layer.LayerType == LayerType.LayerSet:
                in_layer_list.extend(PSFile.get_all_layer(in_layer))

            elif in_layer.LayerType == LayerType.ArtLayer:
                in_layer_list.append(in_layer)

        return in_layer_list

    @staticmethod
    def get_all_layer_set(in_object: CDispatch) -> list:
        """获取所有编组."""
        in_layer_set_list = []
        for in_layer in in_object.LayerSets:
            visible = in_layer.Visible
            if in_layer.AllLocked is True:
                in_layer.AllLocked = False
                in_layer.Visible = visible

            in_layer_set_list.append(in_layer)
            in_layer_set_list.extend(PSFile.get_all_layer_set(in_layer))

        return in_layer_set_list

    def com_删除广告图层(self, all_layers: list[CDispatch]) -> None:
        """根据关键词删除广告."""
        with database:
            include_names: list[IncludeName] = list(IncludeName.select())
            is_names: list[IsName] = list(IsName.select())
            text_replace: list[TextReplaceName] = list(TextReplaceName.select())

        for in_layer in all_layers:
            # 普通图层
            if in_layer.Kind != ArtLayerKind.TextLayer:
                com_普通图层广告(
                    art_layer=in_layer,
                    include_names=include_names,
                    is_names=is_names,
                )
                normal_kind = 17
                if in_layer.Kind == normal_kind:
                    in_layer.Rasterize(5)

            # 文字图层
            else:
                com_文字图层广告(text_layer=in_layer, re_contents=text_replace)

    @staticmethod
    def com_修改所有编组(all_layer_sets: list[CDispatch]) -> None:
        """所有编组改名."""
        for layer_set in all_layer_sets:
            visible = layer_set.Visible
            layer_set.Name = f"组 {layer_set.ID}"
            layer_set.Visible = visible

    def run_删除广告导出PNG(self) -> None:
        """删除广告图层 导出PNG."""
        all_layer_sets = self.get_all_layer_set(in_object=self.doc)
        all_layers = self.get_all_layer(in_object=self.doc)
        self.com_删除广告图层(all_layers=all_layers)
        self.com_修改所有编组(all_layer_sets=all_layer_sets)

        # 导出图层PNG
        all_layers = self.get_all_layer(self.doc)
        all_layer_count = 100
        if len(all_layers) < all_layer_count:
            all_item = run_导出所有图层(
                app=self.app,
                in_doc=self.doc,
                file=Path(self.ps_path),
                layer_list=all_layers,
            )
            for item in all_item:
                img_path = item.img_path
                if img_path.exists() is True:
                    time_out = 0
                    time_out_state = False
                    while img_path.stat().st_size == 0:
                        time.sleep(1)
                        time_out += 1

                        max_time = 60
                        if time_out >= max_time:
                            time_out_state = True
                            break

                    if time_out_state is True:
                        continue

                    img_1 = fun_打开图片(img_path=img_path.as_posix())
                    res = run_对比所有图片(img=img_1, ad_img_list=self.ad_pic_list)
                    if res is True:
                        item.item.Delete()

                    new_name = img_path.with_stem(stem=str(uuid1()))
                    img_path.rename(target=new_name)

        # 导出PNG
        save_path = Path(self.ps_path)
        com_psd导出png(ref_doc=self.doc, file=save_path, ad_layer_name="")
        # 插入广告
        fun_插入广告(self.app, self.doc, self.tb_name, self.ad_layer_name)
        self.doc.Save()
        self.doc.Close(2)

    def run_导出图片添加广告(self) -> None:
        """导出图片 添加二维码广告."""
        save_path = Path(self.ps_path)
        if self.doc.ArtLayers.Count > 0:
            first_layer = self.doc.ArtLayers[0]
            if first_layer.Name in ["SY"] or first_layer.Name[0] == "$":
                first_layer.Delete()

        com_psd导出png(ref_doc=self.doc, file=save_path, ad_layer_name="")

        # 插入广告
        fun_插入广告(self.app, self.doc, self.tb_name, self.pwd.hash("1221"))
        self.doc.Save()
        self.doc.Close(2)

    def run_导出图片(self) -> None:
        """导出PNG图片."""
        if self.doc.ArtLayers.Count > 0:
            first_layer = self.doc.ArtLayers[0]
            if first_layer.Name in ["SY"] or first_layer.Name[0] == "$":
                first_layer.Visible = False
        for layer in self.doc.Layers:
            if layer.Name in ["Resources info (Hide me)"]:
                layer.Visible = False

        save_path = Path(self.ps_path)
        com_psd导出png(ref_doc=self.doc, file=save_path, ad_layer_name="")
        self.doc.Close(2)

    def run_图层改名_导出图片(self) -> None:
        """修改所有图层名称 导出图片."""
        save_path = Path(self.ps_path)
        all_layer_sets = self.get_all_layer_set(self.doc)
        all_layers = self.get_all_layer(self.doc)

        for layer in all_layers:
            if layer.Kind != ArtLayerKind.TextLayer:
                visible = layer.Visible
                layer.Name = f"图层 {layer.ID}"
                layer.Visible = visible

            elif layer.Kind == ArtLayerKind.TextLayer:
                visible = layer.Visible
                layer.Name = f"{layer.TextItem.Contents}"
                layer.Visible = visible

        for layer_set in all_layer_sets:
            visible = layer_set.Visible

            layer_set.Name = f"编组 {layer_set.ID}"
            layer_set.Visible = visible

        com_psd导出png(ref_doc=self.doc, file=save_path, ad_layer_name="")

        # 插入广告
        sec_pass = "1221"  # noqa: S105
        fun_插入广告(self.app, self.doc, self.tb_name, self.pwd.hash(secret=sec_pass))
        self.doc.Save()
        self.doc.Close(2)


if __name__ == "__main__":
    from .fun_对比所有导出的图片 import fun_所有广告图片

    ps = PSFile(
        ps_path=r"F:\小夕素材\10000-10999\10047\10047\小夕素材(14).psd",
        tb_name="小夕素材",
        ad_pic_list=fun_所有广告图片(),
    )

    ps.run_删除广告导出PNG()
