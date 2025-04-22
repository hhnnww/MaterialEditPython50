"""mateiral info."""

from pydantic import BaseModel

from fun_素材文件夹.root_path import RootFolder


class FormatCount(BaseModel):
    """Format count."""

    format: str
    count: int


class MaterialInfo(RootFolder):
    @property
    def file_list(self) -> str:
        """10个 AI 文件."""
        return f"{self.count} 个 {self.format} 文件"

    @property
    def count(self) -> int:
        """Count."""
        return self.__format_count[0].count

    @property
    def format_title(self) -> str:
        """Format title."""
        match self.format:
            case "AI" | "EPS":
                return "AI 矢量设计素材"
            case _:
                return f"{self.__format_count[0].format} 设计素材"

    @property
    def size(self) -> str:
        """Size."""
        size_level = ["B", "KB", "MB", "GB", "TB"]
        size = sum(
            [
                material.path.stat().st_size
                for material in self.mateiral_path.all_material
            ]
        )

        num = 1
        size_level_num = 1024
        while size > size_level_num:
            size /= size_level_num
            num += 1
        size = round(size, 2)
        return f"{size} {size_level[num]}"

    @property
    def format(self) -> str:
        """Format."""
        if "ai" in self.__all_format:
            return "AI"

        return self.__format_count[0].format.upper()

    @property
    def __all_format(self) -> list[str]:
        """All format."""
        return [material.format for material in self.mateiral_path.all_material]

    @property
    def __format_count(self) -> list[FormatCount]:
        """Format count."""
        format_list = [
            FormatCount(format=in_format, count=self.__all_format.count(in_format))
            for in_format in set(self.__all_format)
        ]
        format_list.sort(key=lambda x: x.count, reverse=True)
        return format_list
