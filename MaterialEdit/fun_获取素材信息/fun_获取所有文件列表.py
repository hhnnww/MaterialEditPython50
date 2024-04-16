from pathlib import Path


def fun_获取所有文件列表(material_path: str) -> list[Path]:
    return [obj for obj in Path(material_path).rglob("*") if obj.is_file()]
