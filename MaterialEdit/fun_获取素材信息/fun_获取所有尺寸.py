from pathlib import Path


def fun_获取所有尺寸(all_file: list[Path]):
    size = sum([obj.stat().st_size for obj in all_file])
    size_level = ["bytes", "kb", "mb", "gb"]

    num = 0
    while size > 1024:
        size = size / 1024
        num += 1

    size = round(size, 2)

    return f"{size} {size_level[num].upper()}"
