from .fun_遍历指定文件 import rglob


def fun_删除AI对应的PNG文件(material_path: str):
    ai_file_list = rglob(folder=material_path, suffix=[".ai"])

    for ai_file in ai_file_list:
        pic_suffix = [".png", ".jpg", ".jpeg"]

        for suffix in pic_suffix:
            pic_path = ai_file.with_suffix(suffix)
            if pic_path.exists() is True:
                pic_path.unlink()
