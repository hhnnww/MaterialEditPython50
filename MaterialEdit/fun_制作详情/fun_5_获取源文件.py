from pathlib import Path
from typing import Optional


def fun_获取图片对应的源文件(image_path: str, material_file_list: list[Path]) -> Optional[Path]:
    image_stem = Path(image_path).stem
    for obj in material_file_list:
        if obj.stem in image_stem and len(image_stem) - len(obj.stem) <= 3:
            return obj

    return None
