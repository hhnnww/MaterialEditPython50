from .fun_遍历指定文件 import fun_遍历指定文件


def fun_删除字体文件(material_path: str):
    font_file_list = fun_遍历指定文件(folder=material_path, suffix=[".otf", ".ttf"])
    return font_file_list
