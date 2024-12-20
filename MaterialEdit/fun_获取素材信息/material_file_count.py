"""获取素材源文件的数量."""

from pathlib import Path

from MaterialEdit.setting import MATERIAL_SOURCE_SUFFIX


def mateiral_file_count(file_list: list[Path]) -> list[tuple[int, str]]:
    """获取素材源文件的数量."""
    ma_list = []

    for suffix in MATERIAL_SOURCE_SUFFIX:
        has_suffix_list = [obj for obj in file_list if obj.suffix.lower() == suffix]
        ma_list.append((len(has_suffix_list), suffix.replace(".", "")))

    return [obj for obj in ma_list if obj[0] > 0]
