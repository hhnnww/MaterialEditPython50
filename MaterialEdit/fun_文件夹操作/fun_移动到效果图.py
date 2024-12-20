import shutil
from pathlib import Path

from tqdm import tqdm

from ..setting import IMAGE_SUFFIX
from .fun_单个文件制作WEB预览图 import image_make_web_thumbnail


def fun_移动到效果图(material_path: str, effect_path: str):
    material_path_obj = Path(material_path)
    effect_path_obj = Path(effect_path)

    pic_list: list[Path] = []
    for in_file in material_path_obj.rglob("*"):
        if in_file.is_file() and in_file.suffix.lower() in IMAGE_SUFFIX:
            pic_list.append(in_file)

    if len(pic_list) > 0:
        if effect_path_obj.exists() is False:
            effect_path_obj.mkdir()

    num = 1
    for in_file in tqdm(pic_list, ncols=100, desc="移动到效果图\t"):
        effect_image_path = effect_path_obj / f"{num}{in_file.suffix}"
        while effect_image_path.exists() is True:
            num += 1
            effect_image_path = effect_path_obj / f"{num}{in_file.suffix}"

        shutil.copy(in_file.as_posix(), effect_image_path.as_posix())
        image_make_web_thumbnail(image_path=effect_image_path)
