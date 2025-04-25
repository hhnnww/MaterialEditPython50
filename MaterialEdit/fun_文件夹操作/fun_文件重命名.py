"""文件重命名.py"""

import uuid
from pathlib import Path

from MaterialEdit.setting import IMAGE_SUFFIX, MATERIAL_SOURCE_SUFFIX


def fun_文件重命名(  # noqa: C901, PLR0912
    folder: str,
    preview_path: str,
    shop_name: str,
    num: int = 1,
) -> None:
    """重命名文件夹内的文件."""
    folder_obj = Path(folder)
    preview_path_obj = Path(preview_path)

    all_material_file = [
        in_file
        for in_file in folder_obj.rglob("*")
        if in_file.is_file() and in_file.suffix.lower() in MATERIAL_SOURCE_SUFFIX
    ]
    all_material_file.sort(key=lambda in_list_file: in_list_file.suffix)

    for in_file in all_material_file:
        new_stem = str(uuid.uuid1())
        material_file_new_name = in_file.with_stem(new_stem).with_suffix(
            in_file.suffix.lower(),
        )

        for image_suffix in IMAGE_SUFFIX:
            image_path = in_file.with_suffix(image_suffix)

            if image_path.exists() is True:
                image_file_new_name = image_path.with_stem(new_stem)

                while (
                    image_file_new_name.exists() is True
                    or material_file_new_name.exists() is True
                ):
                    new_stem = str(uuid.uuid1())
                    material_file_new_name = in_file.with_stem(new_stem)
                    image_file_new_name = image_path.with_stem(new_stem)

                image_path.rename(image_file_new_name.as_posix())

        while material_file_new_name.exists() is True:
            new_stem = str(uuid.uuid1())
            material_file_new_name = in_file.with_stem(new_stem)

        for in_preview_image in preview_path_obj.rglob("*"):
            if (
                in_preview_image.stem == in_file.stem
                and in_preview_image.is_file()
                and in_preview_image.suffix.lower() in IMAGE_SUFFIX
            ):
                preview_new_path = in_preview_image.with_stem(new_stem)
                in_preview_image.rename(preview_new_path)

        in_file.rename(material_file_new_name.as_posix())

    for in_file in folder_obj.rglob("*"):
        if in_file.is_file() and in_file.suffix.lower() in MATERIAL_SOURCE_SUFFIX:
            new_stem = f"{shop_name}({num})"
            material_new_name = in_file.with_stem(new_stem)

            for image_suffix in IMAGE_SUFFIX:
                image_path = in_file.with_suffix(image_suffix)
                if image_path.exists() is True:
                    image_new_name = image_path.with_stem(new_stem)
                    image_path.rename(image_new_name)

            for in_prev_img in preview_path_obj.rglob("*"):
                if (
                    in_prev_img.stem == in_file.stem
                    and in_prev_img.suffix.lower() in IMAGE_SUFFIX
                    and in_prev_img.is_file()
                ):
                    in_prev_img_new_name = in_prev_img.with_stem(new_stem)
                    in_prev_img.rename(in_prev_img_new_name)

            in_file.rename(material_new_name)

            num += 1
