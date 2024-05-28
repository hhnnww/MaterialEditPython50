import shutil
from pathlib import Path

from tqdm import tqdm

from ..setting import IMAGE_SUFFIX
from .fun_单个文件制作WEB预览图 import fun_单个文件制作WEB预览图


class ImageCopyToPreview:
    def __init__(self, folder_path: str, preview_path: str) -> None:
        self.folder_path_obj = Path(folder_path)
        self.preview_path_obj = Path(preview_path)

    def all_image(self) -> list[Path]:
        """
        遍历所有图片

        Returns:
            list[Path]: _description_
        """
        pic_list = []
        for in_file in self.folder_path_obj.rglob("*"):
            if in_file.is_file() and in_file.suffix.lower() in IMAGE_SUFFIX:
                pic_list.append(in_file)
        return pic_list

    def image_to_preview_image(self, image_path: Path) -> Path:
        """单个图片转换成预览图图片路径

        Args:
            image_path (Path): 素材文件夹内的图片

        Returns:
            Path: 预览图文件夹内的图片路径
        """
        return Path(
            image_path.as_posix().replace(
                self.folder_path_obj.as_posix(), self.preview_path_obj.as_posix()
            )
        )

    def main(self):
        for image_file in tqdm(self.all_image(), desc="复制图片到预览图", ncols=100):
            preview_file = self.image_to_preview_image(image_file)

            # AI 文件中的 link 文件
            # 不复制
            if image_file.parent.stem.lower() == "links":
                print(f"图片是AI文件夹内的link图片,不复制:{image_file}")
                continue

            # 图片已经存在
            if preview_file.exists() is True:
                print(f"图片纯在不复制:{image_file}")
                continue

            # 图片在子文件夹内
            # 先创建父文件夹
            if preview_file.parent.exists() is False:
                print(f"预览图需要创建父文件夹:{preview_file.parent}")
                preview_file.parent.mkdir(parents=True)

            print(f"复制到预览图:{image_file}\t->\t{preview_file}")

            shutil.copy(image_file, preview_file)
            fun_单个文件制作WEB预览图(image_path=preview_file)
