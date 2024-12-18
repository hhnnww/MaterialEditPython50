import time
from pathlib import Path
from typing import List, Optional
from uuid import uuid1

from colorama import Back, Fore, Style
from win32com.client import CDispatch, Dispatch

# import face_recognition
from .fun_对比所有导出的图片 import fun_打开图片, run_对比所有图片
from .fun_导出PNG import com_psd导出png
from .fun_导出图层PNG import run_导出所有图层
from .fun_插入广告 import fun_插入广告
from .fun_文字图层替换广告 import com_文字图层广告
from .fun_普通图层替换广告 import com_普通图层广告
from .fun_清理注释 import fun_清理注释
from .model import IncludeName, IsName, IsPhoto, TextReplaceName, database


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
        ad_pic_list: Optional[List[Path]] = None,
    ):
        self.ps_path = ps_path
        self.tb_name = tb_name

        self.app = Dispatch("photoshop.application")
        self.app.displayDialogs = 3

        self.app.Open(ps_path)
        self.doc = self.app.ActiveDocument

        self.ad_layer_name = "隐藏 或 删除此图层即可开始您的编辑."
        self.ad_pic_list = ad_pic_list

        fun_清理注释(self.app)
        print(f"\n\n处理PSD:{self.ps_path}")

    @staticmethod
    def get_all_layer(in_object: CDispatch):
        """
        获取所有的图层
        :param in_object:
        :return:
        """
        in_layer_list = []
        for in_layer in in_object.layers:
            # in_layer.Visible = True
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
    def get_all_layer_set(in_object: CDispatch):
        """
        获取所有的编组
        :param in_object:
        :return:
        """
        in_layer_set_list = []
        for in_layer in in_object.LayerSets:
            # in_layer.Visible = True
            visible = in_layer.Visible
            if in_layer.AllLocked is True:
                in_layer.AllLocked = False
                in_layer.Visible = visible

            in_layer_set_list.append(in_layer)
            in_layer_set_list.extend(PSFile.get_all_layer_set(in_layer))

        return in_layer_set_list

    def com_删除广告图层(self, all_layers: List[CDispatch]):
        """
        从数据库获取所有广告语
        根据图层名字删除所有的广告图层
        :param all_layers:
        :return:
        """
        with database:
            include_names: List[IncludeName] = list(IncludeName.select())
            is_names: List[IsName] = list(IsName.select())
            text_replace: List[TextReplaceName] = list(TextReplaceName.select())
            photo_names: List[IsPhoto] = list(IsPhoto.select())

        for in_layer in all_layers:
            # 普通图层
            if in_layer.Kind != ArtLayerKind.TextLayer:
                com_普通图层广告(
                    self.app,  # type: ignore
                    in_layer,
                    include_names,
                    is_names,
                    photo_names,  # type: ignore
                )

                if in_layer.Kind == 17:
                    in_layer.Rasterize(5)

            # 文字图层
            else:
                com_文字图层广告(in_layer, text_replace)

    @staticmethod
    def com_修改所有编组(all_layer_sets: List[CDispatch]):
        for layer_set in all_layer_sets:
            visible = layer_set.Visible
            layer_set.Name = f"组 {layer_set.ID}"
            layer_set.Visible = visible

    def run_删除广告导出PNG(self):
        all_layer_sets = self.get_all_layer_set(self.doc)
        all_layers = self.get_all_layer(self.doc)
        self.com_删除广告图层(all_layers)
        self.com_修改所有编组(all_layer_sets)

        # 导出图层PNG
        all_layers = self.get_all_layer(self.doc)

        if len(all_layers) < 100:
            all_item = run_导出所有图层(
                app=self.app,  # type: ignore
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

                        if time_out >= 60:
                            time_out_state = True
                            break

                    if time_out_state is True:
                        continue

                    img_1 = fun_打开图片(img_path.as_posix())
                    res = run_对比所有图片(img_1, self.ad_pic_list)  # type: ignore
                    if res is True:
                        print(
                            "\n"
                            + Back.RED  # type: ignore
                            + Fore.BLACK
                            + f"对比图片发现广告:\t{item.item.Name}"
                            + Style.RESET_ALL
                        )
                        item.item.Delete()

                    new_name = img_path.with_stem(str(uuid1()))
                    img_path.rename(new_name)

                    # else:
                    #     image = face_recognition.load_image_file(
                    #         img_path.as_posix()
                    #     )
                    #     face_location = face_recognition.face_locations(image)
                    #     if len(face_location) > 0:
                    #         self.doc.ActiveLayer = item.item
                    #         desc234 = Dispatch("Photoshop.ActionDescriptor")
                    #         desc234.PutUnitDouble(
                    #             s(self.app, "radius"),
                    #             s(self.app, "pixelsUnit"),
                    #             50.000000,
                    #         )
                    #         self.app.ExecuteAction(
                    #             s(self.app, "gaussianBlur"), desc234, dialog()
                    #         )

        # 导出PNG
        save_path = Path(self.ps_path)
        print(f'导出PNG:\t{save_path.with_suffix(".png")}')
        com_psd导出png(ref_doc=self.doc, file=save_path, ad_layer_name="")

        # 插入广告
        fun_插入广告(self.app, self.doc, self.tb_name, self.ad_layer_name)

        print(f"保存：\t{save_path.as_posix()}")
        self.doc.Save()

        print(f"关闭：\t{save_path.as_posix()}")
        self.doc.Close(2)

    def run_导出图片添加广告(self):
        save_path = Path(self.ps_path)
        print(f'导出PNG:\t{save_path.with_suffix(".png")}')

        if self.doc.ArtLayers.Count > 0:
            first_layer = self.doc.ArtLayers[0]
            if first_layer.Name in ["SY"]:
                first_layer.Delete()

        com_psd导出png(ref_doc=self.doc, file=save_path, ad_layer_name="")

        # 插入广告
        fun_插入广告(self.app, self.doc, self.tb_name, self.ad_layer_name)

        print(f"保存：\t{save_path.as_posix()}")
        self.doc.Save()

        print(f"关闭：\t{save_path.as_posix()}")
        self.doc.Close(2)

    def run_导出图片(self):
        save_path = Path(self.ps_path)
        print(f'导出PNG:\t{save_path.with_suffix(".png")}')
        com_psd导出png(ref_doc=self.doc, file=save_path, ad_layer_name="")

        # 插入广告
        # fun_插入广告(self.app, self.doc, self.tb_name, self.ad_layer_name)

        # print(f"保存：\t{save_path.as_posix()}")
        # self.doc.Save()

        print(f"关闭：\t{save_path.as_posix()}")
        self.doc.Close(2)

    def run_图层改名_导出图片(self):
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
        fun_插入广告(self.app, self.doc, self.tb_name, self.ad_layer_name)

        print(f"保存：\t{save_path.as_posix()}")
        self.doc.Save()

        print(f"关闭：\t{save_path.as_posix()}")
        self.doc.Close(2)


if __name__ == "__main__":
    from .fun_对比所有导出的图片 import fun_所有广告图片

    ps = PSFile(
        ps_path=r"F:\小夕素材\10000-10999\10047\10047\小夕素材(14).psd",
        tb_name="小夕素材",
        ad_pic_list=fun_所有广告图片(),
    )

    ps.run_删除广告导出PNG()
