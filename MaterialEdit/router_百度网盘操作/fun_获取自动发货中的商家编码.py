import re


def fun_获取自动发货中的商家编码(text: str):
    id_list = re.findall(r"商家编码：(.*?)\n", text)
    return id_list
