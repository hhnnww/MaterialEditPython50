import logging

from colorama import Back, Fore, Style
from win32com.client import CDispatch

from .model import IncludeName, IsName


def com_普通图层广告(
    art_layer: CDispatch,
    include_names: list[IncludeName],
    is_names: list[IsName],
):
    """处理普通图层广告."""
    visible = art_layer.Visible
    layer_name: str = art_layer.Name
    layer_name = layer_name.lower()
    layer_state = 1

    # 删除包含字符
    if layer_state == 1:
        for in_name in include_names:
            if str(in_name.name).lower() in layer_name:
                msg = ("\n" + Back.RED + Fore.BLACK + f"普通图层发现广告:\t{art_layer.Name}" + Style.RESET_ALL,)
                logging.info(msg=msg)

                art_layer.Delete()
                layer_state = 0
                break

    # 删除等于字符
    if layer_state == 1:
        for in_name in is_names:
            if str(in_name.name).lower() == layer_name:
                msg = ("\n" + Back.RED + Fore.BLACK + f"普通图层发现广告:\t{art_layer.Name}" + Style.RESET_ALL,)
                logging.info(msg=msg)
                art_layer.Delete()
                layer_state = 0
                break

    # 修改名字
    if layer_state == 1:
        art_layer.Name = f"图层 {art_layer.ID}"
        art_layer.Visible = visible
