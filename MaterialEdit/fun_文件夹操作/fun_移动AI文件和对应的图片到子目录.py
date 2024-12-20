"""吧AI文件和对应的PNG图片移动到子目录."""

from pathlib import Path

from MaterialEdit.setting import IMAGE_SUFFIX


class AIFile:
    """ai单个文件."""

    def __init__(self, ai_file: Path, all_image: list[Path]) -> None:
        """ai文件."""
        self.ai_file = ai_file
        self.all_image = all_image

    @property
    def image_file_list(self) -> list[Path]:
        """ai对应的图片列表."""
        return [image for image in self.all_image if self.ai_file.stem in image.name]

    @property
    def sub_path(self) -> Path:
        """AI文件需要移动的子目录."""
        return self.ai_file.parent / self.ai_file.stem

    def move_ai_file(self) -> None:
        """移动AI文件."""
        if self.sub_path.exists() is not True:
            self.sub_path.mkdir()

        self.ai_file.rename(target=self.sub_path / self.ai_file.name)

    def move_image_file(self) -> None:
        """移动所有的图片文件."""
        for image in self.image_file_list:
            image.rename(target=self.sub_path / image.name)


class MoveAIToSubPath:
    """画册AI素材对应的图片太多.

    需要移动AI文件和对应的图片文件列表到子目录.
    """

    def __init__(self, material_path_str: str) -> None:
        """素材文件夹目录."""
        self.material_path = Path(material_path_str)

    @property
    def all_image(self) -> list[Path]:
        """素材文件夹内的所有图片."""
        return [
            image
            for image in self.material_path.iterdir()
            if image.is_file() and image.suffix.lower() in IMAGE_SUFFIX
        ]

    @property
    def all_ai_file(self) -> list[AIFile]:
        """所有的ai文件."""
        return [
            AIFile(ai_file=ai_file, all_image=self.all_image)
            for ai_file in self.material_path.iterdir()
            if ai_file.is_file() and ai_file.suffix.lower() in [".ai"]
        ]

    def main(self) -> None:
        """移动所有文件."""
        for obj in self.all_ai_file:
            obj.move_ai_file()
            obj.move_image_file()


if __name__ == "__main__":
    MoveAIToSubPath(material_path_str=r"F:\小夕素材\10000-20000\10961\10961").main()
