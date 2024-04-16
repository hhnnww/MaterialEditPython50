from typing import List

from colorama import Back, Fore
from colorama import Style
from win32com.client import CDispatch

from .model import TextReplaceName


def com_文字图层广告(text_layer: CDispatch, re_contents: List[TextReplaceName]):
    visible = text_layer.Visible
    text_item = text_layer.TextItem
    content: str = text_item.Contents
    content = content.lower()
    new_name = content.replace("\r", "")

    for tr in re_contents:
        ori_name = str(tr.ori_name).lower()
        text_item = text_layer.TextItem
        content: str = text_item.Contents
        content = content.lower()

        if ori_name in content:
            try:
                print("\n" + Back.RED + Fore.BLACK + f"文字图层发现广告：\t{text_layer.Name}" + Style.RESET_ALL)
            except:
                pass

            if "bold" in str(text_item.Font).lower():
                text_item.Font = "AlibabaPuHuiTi_2_65_Medium"
            else:
                text_item.Font = "AlibabaPuHuiTi_2_45_Light"

            new_content = content.replace(tr.ori_name, tr.dst_name)
            text_item.Contents = new_content

            new_name = new_content.replace("\r", "")

    # 改名字
    text_layer.Name = new_name
    text_layer.Visible = visible
