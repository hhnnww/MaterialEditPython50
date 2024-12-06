import re
from pathlib import Path
from typing import Optional

from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import fun_遍历指定文件


class SDPicReName:
    def __init__(self, material_path: str, shop_name: str, effect_path: str) -> None:
        self.material_path = material_path
        self.shop_name = shop_name
        self.effect_path = effect_path

    def name_replace(self, old_stem: str) -> Optional[str]:
        re_name = re.findall(rf".*({self.shop_name}.*)", old_stem)
        if re_name:
            return re_name[0]

        raise IndexError(f"{old_stem}:\t效果图文件名没有找到店铺名")

    def main(self):
        all_file = fun_遍历指定文件(folder=self.effect_path, suffix=[".png"])
        for in_file in all_file:
            new_stem = self.name_replace(in_file.stem)
            if new_stem:
                new_path = in_file.with_stem(new_stem)
                if new_path.exists() is not True:
                    in_file.rename(new_path)

        # 删除素材文件夹的所有图片
        ma_png_list = fun_遍历指定文件(folder=self.material_path, suffix=[".png"])
        for ma_png in ma_png_list:
            ma_png.unlink()

        # 遍历源文件和效果图
        ma_file_list = fun_遍历指定文件(folder=self.material_path, suffix=[".skp"])
        effect_png_file = fun_遍历指定文件(folder=self.effect_path, suffix=[".png"])

        for effect_png in effect_png_file:
            for ma_file in ma_file_list:
                if effect_png.stem == ma_file.stem:
                    new_path = ma_file.parent / effect_png.name
                    effect_png.rename(new_path)

        Path(self.effect_path).unlink()
