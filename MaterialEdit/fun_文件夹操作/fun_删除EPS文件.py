from .fun_遍历指定文件 import fun_遍历指定文件


def fun_删除EPS文件(material_path: str):
    ai_file_list = fun_遍历指定文件(folder=material_path, suffix=[".ai"])
    eps_file_list = fun_遍历指定文件(folder=material_path, suffix=[".eps"])

    if len(ai_file_list) == len(eps_file_list):
        for in_file in eps_file_list:
            in_file.unlink()
