from .fun_遍历指定文件 import rglob


def fun_删除字体文件(material_path: str):
    font_file_list = rglob(folder=material_path, suffix=[".otf", ".ttf"])
    return font_file_list
