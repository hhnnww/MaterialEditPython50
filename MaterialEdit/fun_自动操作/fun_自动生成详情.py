from pathlib import Path

from tqdm import tqdm

from MaterialEdit import fun_获取素材信息
from Router.fun_制作详情 import (
    MakeProductImageRequestModel,
    fun_make_material_product_image,
)

from ..fun_获取路径数字 import fun_获取路径数字
from .fun_判断文件夹是否为空 import fun_判断是否为空文件夹


class AutoMakeProductImage:
    def __init__(self, material_parent_path: str, start_stem: int, shop_name: str):
        self.parent_path = Path(material_parent_path)
        self.start_id = start_stem
        self.shop_name = shop_name

    def fun_生成文件夹列表(self):
        path_list = []
        for in_path in list(self.parent_path.iterdir()):
            if in_path.is_dir() and fun_获取路径数字(in_path.stem) >= self.start_id:
                path_list.append(in_path)

        return path_list

    def fun_生成单个详情(self, root_path: Path):
        ma_info = fun_获取素材信息(
            root_path=root_path.as_posix(), used_image=0, image_sort=True
        )

        oneline_number = 2
        oneline_ratio = 2.5

        if ma_info.preview_image_count > 50:
            oneline_number = 3
            oneline_ratio = 3.5

        elif ma_info.preview_image_count > 100:
            oneline_number = 4
            oneline_ratio = 4.5

        fun_make_material_product_image(
            item=MakeProductImageRequestModel(
                shop_name=self.shop_name,
                material_path=ma_info.material_path,
                preview_image_path=ma_info.preview_image_path,
                effect_image_path=ma_info.effect_image_path,
                # 数据图
                material_id=ma_info.material_id,
                material_source_file_size=ma_info.material_source_file_size,
                material_source_format_title=ma_info.material_source_format_title,
                material_source_format_number=ma_info.material_source_format_number,
                # 制作详情
                oneline_number=oneline_number,
                oneline_ratio=oneline_ratio,
                has_preview_image=True,
                has_effect_image=True,
                preview_image_sort=True,
                preview_used_number=0,
                preview_has_material_info=True,
                preview_image_count=len(ma_info.preview_image_list),
                crop_position="start",
                xq_width=1500,
                save_sub_path=True,
            )
        )

    def run(self):
        path_list = self.fun_生成文件夹列表()
        for root_path in tqdm(path_list, ncols=100, desc="生成详情\t"):
            if fun_判断是否为空文件夹(root_path) is True:
                print(root_path)
                self.fun_生成单个详情(root_path)
