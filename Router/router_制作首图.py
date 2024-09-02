from fastapi import APIRouter
from MaterialEdit import (
    ImageEdit,
    LayoutAdaptiveCrop,
    fun_layout_1_2_3,
    fun_layout_1_2_3_3,
    fun_layout_1_n,
    fun_layout_固定裁剪2,
    fun_T500首图,
    fun_保存图片,
    fun_清空桌面上传文件夹图片,
    fun_黑鲸首图,
    layout_s1_n,
)
from MaterialEdit.fun_制作首图.layout_1_2_3_3_3 import fun_layout_1_2_3_3_3
from MaterialEdit.fun_制作首图.layout_错乱排列.class_random_auto_layout import (
    RandomAutoLayout,
)
from MaterialEdit.fun_制作首图.layout_错乱排列.class_random_layout import (
    LayoutRandomLayoug,
)
from MaterialEdit.type import ALIGNITEM, ImageModel
from pydantic import BaseModel

router = APIRouter(prefix="/MakeFirstImage")


class MakeFirstImageModel(BaseModel):
    first_image_title: str
    select_image_list: list[ImageModel]

    first_image_style: str
    first_image_line: int
    first_image_layout: str
    crop_position: ALIGNITEM

    first_image_num: str
    spacing: int

    format_title: str
    material_id: str
    shop_name: str
    source_format: str


@router.post("")
def make_first_image(item: MakeFirstImageModel):
    fun_清空桌面上传文件夹图片("st_" + item.first_image_num)

    # 制作首图背景
    xq_width, xq_height = 1500, 1500

    if item.first_image_style == "黑鲸":
        xq_height = 1300

    if item.first_image_layout == "自适应裁剪":
        bg = LayoutAdaptiveCrop(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            line=item.first_image_line,
            spacing=item.spacing,
            crop_position=item.crop_position,
        ).run_制作自适应布局图片()

    elif item.first_image_layout == "1-2":
        bg = fun_layout_1_n(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            small_line_num=2,
        )

    elif item.first_image_layout == "1-3":
        bg = fun_layout_1_n(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            small_line_num=3,
        )

    elif item.first_image_layout == "1-4":
        bg = fun_layout_1_n(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            small_line_num=4,
        )

    elif item.first_image_layout == "1-2-3":
        bg = fun_layout_1_2_3(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
        )

    elif item.first_image_layout == "1-2-3-3":
        bg = fun_layout_1_2_3_3(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
        )
    elif item.first_image_layout == "1-2-3-3-3":
        bg = fun_layout_1_2_3_3_3(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
        )

    elif item.first_image_layout == "S1-2":
        bg = layout_s1_n(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=2,
        )

    elif item.first_image_layout == "S1-3":
        bg = layout_s1_n(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=3,
        )

    elif "错乱" in item.first_image_layout and "全自动" not in item.first_image_layout:
        bg = LayoutRandomLayoug(
            image_list=[obj.path for obj in item.select_image_list],
            layout_str=item.first_image_layout,
            width=xq_width,
            height=xq_height,
            crop_position=item.crop_position,
        ).main()

    elif "错乱" in item.first_image_layout and "全自动" in item.first_image_layout:
        bg = RandomAutoLayout(
            image_list=[obj.path for obj in item.select_image_list],
            width=xq_width,
            height=xq_height,
            line_row=item.first_image_line,
        ).main()

    else:
        bg = fun_layout_固定裁剪2(
            image_list=item.select_image_list,
            line=item.first_image_line,
            spacing=item.spacing,
            crop_position=item.crop_position,
            xq_width=xq_width,
            xq_height=xq_height,
        )

    # 开始制作首图样式
    water_pixel_color = int(255 * 0.7)
    bg = ImageEdit.fun_图片打满水印(
        bg,
        60,
        5,
        5,
        (water_pixel_color, water_pixel_color, water_pixel_color, int(255 * 0.8)),
    )

    if item.first_image_style == "T500":
        bg = fun_T500首图(
            im=bg,
            title=item.first_image_title,
            format_title=item.format_title,
            shop_name=item.shop_name,
            material_id=item.material_id,
        )

    elif item.first_image_style == "黑鲸":
        bg = fun_黑鲸首图(
            im=bg,
            title=item.first_image_title,
            material_format=item.source_format,
            material_id=item.material_id,
        )

    fun_保存图片(bg, "st_" + item.first_image_num)

    return dict(msg="ok")
