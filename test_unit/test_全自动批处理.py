from pathlib import Path
from tqdm import tqdm
from MaterialEdit.fun_获取路径数字 import fun_获取路径数字
from Router.router_文件夹操作 import RequestMaterialPathActionModel, fun_material_path_action
from pprint import pprint


def fun_处理单个文件(shop_name: str, root_path: str):
    for action_list in [
        "解压ZIP",
        "删除EPS文件",
        "移动到效果图",
        "文件重命名",
        "移动到根目录",
        "删除广告文件",
        "AI-导出图片",
        "PSD-导出图片-添加广告",
        "复制图片到预览图",
        "素材图水印",
    ]:
        item = RequestMaterialPathActionModel(action=action_list, shop_name=shop_name, root_path=root_path)
        fun_material_path_action(item=item)


def fun_获取所有需要处理的文件夹(parent_path: str, start_stem: int):
    all_file = list(Path(parent_path).iterdir())
    used_folder = []

    for in_file in all_file:
        if in_file.is_dir() and fun_获取路径数字(in_file.stem) >= start_stem:
            used_folder.append(in_file.as_posix())

    used_folder.sort(key=lambda k: fun_获取路径数字(Path(k).stem))

    return used_folder


if __name__ == "__main__":
    for in_file in tqdm(fun_获取所有需要处理的文件夹(parent_path=r"G:\饭桶设计\2000-2999", start_stem=2876), ncols=100, desc="处理文件夹\t"):
        print(in_file)
        fun_处理单个文件(shop_name="饭桶设计", root_path=in_file)
