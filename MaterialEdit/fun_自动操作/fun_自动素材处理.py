from pathlib import Path

from tqdm import tqdm

from Router.router_文件夹操作 import RequestMaterialPathActionModel, fun_material_path_action
from ..fun_获取路径数字 import fun_获取路径数字


class AutoMaterialFileEdit:
    def __init__(self, shop_name: str, parent_path: str, start_stem: int):
        self.shop_name = shop_name
        self.parent_path = parent_path
        self.start_stem = start_stem

    def fun_处理单个文件(self, root_path: str):
        for action_list in [
            # "解压ZIP",
            # "删除EPS文件",
            "删除ZIP文件",
            # "移动到效果图",
            "删除素材文件夹内所有图片",
            "文件重命名",
            "移动到根目录",
            "删除广告文件",
            # "AI-导出图片",
            "PSD-图层改名-导出图片-添加广告",
            "复制图片到预览图",
            "素材图水印",
        ]:
            item = RequestMaterialPathActionModel(action=action_list, shop_name=self.shop_name, root_path=root_path)
            fun_material_path_action(item=item)

    def fun_获取所有需要处理的文件夹(self):
        all_file = list(Path(self.parent_path).iterdir())
        used_folder = []

        for in_file in all_file:
            if in_file.is_dir() and fun_获取路径数字(in_file.stem) >= self.start_stem:
                used_folder.append(in_file.as_posix())

        used_folder.sort(key=lambda k: fun_获取路径数字(Path(k).stem))

        return used_folder

    def run(self):
        for in_file in tqdm(self.fun_获取所有需要处理的文件夹(), ncols=100, desc="处理文件夹\t"):
            print(in_file)
            self.fun_处理单个文件(root_path=in_file)
