from pathlib import Path

from ..setting import MATERIAL_SOURCE_SUFFIX


def fun_获取源文件数量(file_list: list[Path]) -> list[tuple[int, str]]:
    l = []

    for suffix in MATERIAL_SOURCE_SUFFIX:
        has_suffix_list = [obj for obj in file_list if obj.suffix.lower() == suffix]
        l.append((len(has_suffix_list), suffix.replace(".", "")))

    return [obj for obj in l if obj[0] > 0]
