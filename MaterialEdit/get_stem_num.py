"""从文件的stem中获取数字."""

import re


def get_path_num(stem: str) -> int:
    """获取文件名中的数字."""
    if "(" in stem and ")" in stem:
        num_list = re.findall(r"\((\d+)\)", stem)
    else:
        num_list = re.findall(r"(\d+)", stem)

    if len(num_list) > 0:
        return int("".join(num_list))

    return 0
