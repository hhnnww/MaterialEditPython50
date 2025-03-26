"""删除指定文件夹中与 .ai 文件同名的图片文件（支持 .png、.jpg、.jpeg 格式）。

遍历指定文件夹中的所有 .ai 文件。
"""

from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob


def fun_删除AI对应的PNG文件(material_path: str) -> None:
    """删除指定文件夹中与 .ai 文件同名的图片文件（支持 .png、.jpg、.jpeg 格式）。

    参数:
        material_path (str): 要操作的文件夹路径。
    功能:
        遍历指定文件夹中的所有 .ai 文件
        检查是否存在与其同名的 .png、.jpg 或 .jpeg 文件。
        如果存在，则删除这些图片文件。
    注意:
        该函数会直接删除文件，请谨慎使用。
    """
    ai_file_list = rglob(folder=material_path, suffix=[".ai"])

    for ai_file in ai_file_list:
        pic_suffix = [".png", ".jpg", ".jpeg"]

        for suffix in pic_suffix:
            pic_path = ai_file.with_suffix(suffix)
            if pic_path.exists() is True:
                pic_path.unlink()
