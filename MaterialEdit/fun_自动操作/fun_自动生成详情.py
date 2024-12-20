from pathlib import Path

from tqdm import tqdm

from MaterialEdit import fun_获取素材信息
from MaterialEdit.router_制作详情2.fun_制作详情2 import (
    MakeProductImageRequestModel,
    fun_制作详情2,
)

from ..get_stem_num import get_path_num
from .fun_判断文件夹是否为空 import fun_判断是否为空文件夹


class AutoMakeProductImage:
    def __init__(
        self,
        material_parent_path: str,
        start_stem: int,
        shop_name: str,
        make_effect: bool,
    ):
        self.parent_path = Path(material_parent_path)
        self.start_id = start_stem
        self.shop_name = shop_name
        self.make_effect = make_effect

    def fun_生成文件夹列表(self):
        path_list = []
        for in_path in list(self.parent_path.iterdir()):
            if in_path.is_dir() and get_path_num(in_path.stem) >= self.start_id:
                path_list.append(in_path)

        return path_list

    def fun_生成单个详情(self, root_path: Path):
        ma_info = fun_获取素材信息(
            root_path=root_path.as_posix(),
            used_image=0,
            image_sort=True,
        )

        # pic_list = [ImageModel(**obj) for obj in ma_info.preview_image_list]
        # for x in range(4):
        #     st = Layout列固定尺寸(
        #         image_list=pic_list,
        #         col=3,
        #         xq_width=1500,
        #         xq_height=1500,
        #         spacing=10,
        #         crop_position="center",
        #         bg_color=(255, 255, 255, 255),
        #     ).main()
        #     fun_保存图片(
        #         im=st, material_id=f"st-{ma_info.material_id}_{x+1}", stem="st"
        #     )
        #     random.shuffle(pic_list)

        oneline_number = 1
        oneline_ratio = 2.5

        if ma_info.preview_image_count > 40:
            oneline_number = 2
            oneline_ratio = 2.5

        elif ma_info.preview_image_count > 80:
            oneline_number = 3
            oneline_ratio = 3.5

        elif ma_info.preview_image_count > 100:
            oneline_number = 4
            oneline_ratio = 4.5

        fun_制作详情2(
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
                # 预览图和效果图
                has_preview_image=True,
                has_effect_image=self.make_effect,
                preview_image_sort=True,
                preview_used_number=0,
                preview_has_material_info=True,
                preview_image_count=len(ma_info.preview_image_list),
                crop_position="start",
                xq_width=1500,
                image_name_has_material_id=True,
                clear_upload_path=False,
                has_water=self.shop_name in ["泡泡素材", "小夕素材", "松子素材"],
            ),
        )

    def run(self):
        path_list = self.fun_生成文件夹列表()
        for root_path in tqdm(path_list, ncols=100, desc="生成详情\t"):
            if fun_判断是否为空文件夹(root_path) is True:
                print(root_path)
                self.fun_生成单个详情(root_path)
