"""获取所有文件."""

from pathlib import Path


def material_file_list(material_path: str) -> list[Path]:
    """获取素材文件夹里面的所有文件."""
    return [obj for obj in Path(material_path).rglob("*") if obj.is_file()]
