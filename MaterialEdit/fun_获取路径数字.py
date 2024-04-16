import re


def fun_获取路径数字(stem: str):
    if "(" in stem and ")" in stem:
        num_list = re.findall(r"\((\d+)\)", stem)
    else:
        num_list = re.findall(r"(\d+)", stem)

    if len(num_list) > 0:
        return int("".join(num_list))

    return 0
