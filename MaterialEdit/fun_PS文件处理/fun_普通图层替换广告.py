from typing import List

from colorama import Back, Fore, Style
from win32com.client import CDispatch

from .model import IncludeName, IsName, IsPhoto


def com_普通图层广告(
    app: CDispatch,
    art_layer: CDispatch,
    include_names: List[IncludeName],
    is_names: List[IsName],
    photo_names: List[IsPhoto],
):
    visible = art_layer.Visible
    layer_name: str = art_layer.Name
    layer_name = layer_name.lower()
    layer_state = 1

    # 删除包含字符
    if layer_state == 1:
        for in_name in include_names:
            if str(in_name.name).lower() in layer_name:
                print(
                    "\n"
                    + Back.RED
                    + Fore.BLACK
                    + f"普通图层发现广告：\t{art_layer.Name}"
                    + Style.RESET_ALL
                )
                art_layer.Delete()
                layer_state = 0
                break

    # 删除等于字符
    if layer_state == 1:
        for in_name in is_names:  # type:ignore
            if str(in_name.name).lower() == layer_name:
                print(
                    "\n"
                    + Back.RED
                    + Fore.BLACK
                    + f"普通图层发现广告：\t{art_layer.Name}"
                    + Style.RESET_ALL
                )
                art_layer.Delete()
                layer_state = 0
                break

    # 高斯模糊
    # if layer_state == 1:
    #     for in_name in photo_names:
    #         if in_name.name in art_layer.Name:
    #             print('\n' + Back.RED + Fore.BLACK + f"普通图层发现广告：\t{art_layer.Name}" + Style.RESET_ALL)
    #             # 高斯模糊
    #             desc234 = Dispatch("Photoshop.ActionDescriptor")
    #             desc234.PutUnitDouble(app.StringIDToTypeID("radius"), app.StringIDToTypeID("pixelsUnit"), 50.000000)
    #             app.ExecuteAction(app.StringIDToTypeID("gaussianBlur"), desc234, 3)

    # 修改名字
    if layer_state == 1:
        art_layer.Name = f"图层 {art_layer.ID}"
        art_layer.Visible = visible
