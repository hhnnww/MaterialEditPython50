"""把素材文件夹图片复制到预览图."""

import logging
import shutil
from pathlib import Path

from tqdm import tqdm

from MaterialEdit.fun_文件夹操作.fun_单个文件制作WEB预览图 import (
    image_make_web_thumbnail,
)
from MaterialEdit.setting import IMAGE_SUFFIX


class ImageCopyToPreview:
    def __init__(self, folder_path: str, preview_path: str) -> None:
        """素材文件夹，预览图文件夹."""
        self.folder_path_obj = Path(folder_path)
        self.preview_path_obj = Path(preview_path)

    def all_image(self) -> list[Path]:
        """遍历所有图片

        Returns:
            list[Path]: _description_

        """
        return [
            in_file
            for in_file in self.folder_path_obj.rglob("*")
            if in_file.is_file() and in_file.suffix.lower() in IMAGE_SUFFIX
        ]

    def image_to_preview_image(self, image_path: Path) -> Path:
        """单个图片转换成预览图图片路径

        Args:
            image_path (Path): 素材文件夹内的图片

        Returns:
            Path: 预览图文件夹内的图片路径

        """
        return Path(
            image_path.as_posix().replace(
                self.folder_path_obj.as_posix(),
                self.preview_path_obj.as_posix(),
            ),
        )

    def one_image_move(self, image_file: Path) -> None:
        """单个图片移动."""
        preview_file = self.image_to_preview_image(image_file)
        if image_file.parent.stem.lower() == "links":
            msg = f"图片是AI文件夹内的link图片,不复制:{image_file}"
            logging.info(msg=msg)
            return

        # 图片已经存在
        if preview_file.exists() is True:
            msg = f"图片纯在不复制:{image_file}"
            logging.info(msg=msg)
            return

        # 图片在子文件夹内
        # 先创建父文件夹
        if preview_file.parent.exists() is False:
            msg = f"预览图需要创建父文件夹:{preview_file.parent}"
            logging.info(msg=msg)
            preview_file.parent.mkdir(parents=True)

        msg = f"复制到预览图:{image_file}\t->\t{preview_file}"
        logging.info(msg=msg)

        shutil.copy(src=image_file, dst=preview_file)
        image_make_web_thumbnail(image_path=preview_file)

    def main(self) -> None:
        """开始移动."""
        for image_file in tqdm(self.all_image(), desc="复制图片到预览图", ncols=100):
            self.one_image_move(image_file=image_file)
