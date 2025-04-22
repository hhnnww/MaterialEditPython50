"""制作首图路由."""

from fastapi import APIRouter
from PIL import Image, ImageColor
from pydantic import BaseModel

from MaterialEdit import (
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
from MaterialEdit.fun_创建文件夹结构 import fun_创建文件夹结构
from MaterialEdit.fun_制作首图 import (
    Layout1大3小自适应,
    Layout1大N行自适应,
    Layout1大竖2排小竖,
    Layout2大竖4小竖,
    LayoutOneLargeTwoSmall,
    Layout列固定尺寸,
    Layout超长图拼接,
    style_paopao,
)
from MaterialEdit.fun_制作首图.layout_1_2_3_3_3 import fun_layout_1_2_3_3_3
from MaterialEdit.fun_制作首图.layout_1_2_3_3_3_3 import fun_layout_1_2_3_3_3_3
from MaterialEdit.fun_制作首图.layout_1_3__2 import Layout13_2
from MaterialEdit.fun_制作首图.layout_1大_33_正方形 import Layout1Large3Small
from MaterialEdit.fun_制作首图.layout_3列1大横竖错落 import layout_3列1大横竖错落
from MaterialEdit.fun_制作首图.layout_3列横竖错落 import layout_3列横竖错落
from MaterialEdit.fun_制作首图.layout_中间大四边小 import LayoutOneLargeOutSmall
from MaterialEdit.fun_制作首图.layout_列自适应 import layout_列自适应
from MaterialEdit.fun_制作首图.layout_圆角固定裁剪 import LayoutRadioCrop
from MaterialEdit.fun_制作首图.layout_小元素排列 import Layout小元素排列
from MaterialEdit.fun_制作首图.layout_横版1212 import Layout1212
from MaterialEdit.fun_制作首图.layout_横版1221 import LayoutHorizontal1221
from MaterialEdit.fun_制作首图.layout_竖横竖竖 import layout_竖横竖竖
from MaterialEdit.fun_制作首图.layout_竖版1221 import Layout竖版1221
from MaterialEdit.fun_制作首图.layout_背景图排版 import Layout背景图排版
from MaterialEdit.fun_制作首图.layout_行_自适应_固定尺寸 import Layout行自适应
from MaterialEdit.fun_制作首图.layout_错乱排列.class_random_auto_layout import (
    RandomAutoLayout,
)
from MaterialEdit.fun_制作首图.layout_错乱排列.class_random_layout import (
    LayoutRandomLayoug,
)
from MaterialEdit.fun_制作首图.style_黑鲸笔刷 import Style黑鲸笔刷
from MaterialEdit.fun_制作首图.style_黑鲸高 import style_黑鲸高
from MaterialEdit.type import ALIGNITEM, ImageModel

router = APIRouter(prefix="/MakeFirstImage")


class MakeFirstImageModel(BaseModel):
    root_path: str

    first_image_title: str
    select_image_list: list[ImageModel]

    first_image_style: str
    first_image_resize: str
    first_image_line: int
    first_image_layout: str
    crop_position: ALIGNITEM

    first_image_num: str
    spacing: int

    format_title: str
    material_id: str
    shop_name: str
    source_format: str

    source_count: str

    bg_color: str

    out_space: int
    radio: int


def fun_换算图片高度(first_image_style_name: str) -> int:
    """根据首图样式，换算首图高度。"""
    xq_height = 1500

    if first_image_style_name == "黑鲸":
        xq_height = 1300
    elif first_image_style_name == "黑鲸高":
        xq_height = 1250
    elif first_image_style_name == "泡泡":
        xq_height = 1200
    elif first_image_style_name == "黑鲸笔刷":
        xq_height = 1000

    return xq_height


@router.post("")
def make_first_image(item: MakeFirstImageModel) -> dict[str, str]:
    """制作首图路由."""
    path_jiegou = fun_创建文件夹结构(root_path=item.root_path)

    """制作首图函数."""
    fun_清空桌面上传文件夹图片("st_" + item.first_image_num)

    # 转换bg_color
    bg_color = ImageColor.getrgb(f"#{item.bg_color}")

    # 制作首图背景
    xq_width = 1500
    xq_height = fun_换算图片高度(first_image_style_name=item.first_image_style)

    if item.first_image_layout == "自适应裁剪":
        bg = LayoutAdaptiveCrop(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            line=item.first_image_line,
            spacing=item.spacing,
            crop_position=item.crop_position,
        ).run_制作自适应布局图片()

    elif item.first_image_layout == "列-固定尺寸":
        bg = Layout列固定尺寸(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=item.first_image_line,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main()

    elif item.first_image_layout == "竖橫竖竖":
        bg = layout_竖横竖竖(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
        )

    elif item.first_image_layout == "1-2":
        bg = fun_layout_1_n(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            small_line_num=2,
        )

    elif item.first_image_layout == "1-3":
        # bg = fun_layout_1_n(
        #     image_list=item.select_image_list,
        #     xq_width=xq_width,
        #     xq_height=xq_height,
        #     spacing=item.spacing,
        #     small_line_num=3,
        # )

        bg = Layout13_2(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=2,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main()

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
            radio=item.radio == 1,
            bg_color=bg_color,
        )

    elif item.first_image_layout == "1-2-3-3-3":
        bg = fun_layout_1_2_3_3_3(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            bg_color=bg_color,
            radio=item.radio == 1,
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

    elif item.first_image_layout == "3列横竖错落":
        bg = layout_3列横竖错落(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
        )

    elif item.first_image_layout == "3列1大横竖错落":
        bg = layout_3列1大横竖错落(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
        )

    elif item.first_image_layout == "列-自适应":
        bg = layout_列自适应(
            image_list=item.select_image_list,
            col=item.first_image_line,
            xq_height=xq_height,
            xq_width=xq_width,
            spacing=item.spacing,
            crop_position=item.crop_position,
            design_path=path_jiegou.design_path,
        )

    elif item.first_image_layout == "1大2行2列":
        bg = LayoutOneLargeTwoSmall(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=2,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main()

    elif item.first_image_layout == "1大3行2列":
        bg = LayoutOneLargeTwoSmall(
            image_list=item.select_image_list,
            bg_color=bg_color,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=3,
            crop_position=item.crop_position,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main()

    elif item.first_image_layout == "1大N行-自适应":
        bg = Layout1大N行自适应(
            image_list=item.select_image_list,
            bg_color=bg_color,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=0,
            crop_position=item.crop_position,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main()

    elif item.first_image_layout == "1竖-2排小竖-自适应":
        bg = Layout1大竖2排小竖(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=0,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main()

    elif item.first_image_layout == "1大3小-自适应":
        bg = Layout1大3小自适应(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=0,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main()

    elif item.first_image_layout == "2大竖-4小竖":
        bg = Layout2大竖4小竖(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=0,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).fun_底部图片()

    elif item.first_image_layout == "超长图":
        bg = Layout超长图拼接(
            image_list=item.select_image_list,
            bg_color=bg_color,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=item.first_image_line,
            crop_position=item.crop_position,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main()

    elif item.first_image_layout == "背景图":
        bg = Layout背景图排版(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=item.first_image_line,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main()

    elif item.first_image_layout == "行-自适应":
        bg = Layout行自适应(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=item.first_image_line,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main(small_size="自适应")

    elif item.first_image_layout == "行-固定尺寸":
        bg = Layout行自适应(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=item.first_image_line,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main(small_size="固定尺寸")

    elif item.first_image_layout == "小元素排列":
        bg = Layout小元素排列(
            image_list=item.select_image_list,
            bg_color=bg_color,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=item.first_image_line,
            crop_position=item.crop_position,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main()

    elif item.first_image_layout == "横版-1221":
        bg = LayoutHorizontal1221(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=item.first_image_line,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).fun_横版1221()

    elif item.first_image_layout == "竖版-1221":
        bg = Layout竖版1221(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=item.first_image_line,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).fun_竖版1221()
    elif item.first_image_layout == "1-2-3-3-3-3":
        bg = fun_layout_1_2_3_3_3_3(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
        )
    elif item.first_image_layout == "中间大四周小":
        bg = LayoutOneLargeOutSmall(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=item.first_image_line,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main()
    elif item.first_image_layout == "1大33正方形":
        bg = Layout1Large3Small(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=item.first_image_line,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main()
    elif item.first_image_layout == "横版-1212":
        bg = Layout1212(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=item.first_image_line,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main()
    elif item.first_image_layout == "固定裁剪-圆角":
        bg = LayoutRadioCrop(
            image_list=item.select_image_list,
            xq_width=xq_width,
            xq_height=xq_height,
            spacing=item.spacing,
            col=item.first_image_line,
            crop_position=item.crop_position,
            bg_color=bg_color,
            out_space=item.out_space == 1,
            design_path=path_jiegou.design_path,
            radio=item.radio == 1,
        ).main()
    else:
        bg = fun_layout_固定裁剪2(
            image_list=item.select_image_list,
            line=item.first_image_line,
            spacing=item.spacing,
            crop_position=item.crop_position,
            xq_width=xq_width,
            xq_height=xq_height,
            design_path=path_jiegou.design_path,
        )

    # ---------------- 样式 ----------------

    if item.first_image_style == "T500":
        bg = fun_T500首图(
            im=bg,
            title=item.first_image_title,
            format_title=item.format_title,
            shop_name=item.shop_name,
            material_id=item.material_id,
            bg_color=bg_color,
        )

    elif item.first_image_style == "黑鲸":
        bg = fun_黑鲸首图(
            im=bg,
            title=item.first_image_title,
            material_format=item.source_format,
            material_id=item.material_id,
            bg_color=bg_color,
            shop_name=item.shop_name,
        )

    elif item.first_image_style == "泡泡":
        bg = style_paopao(
            im=bg,
            title=item.first_image_title,
            material_format=item.source_format,
            material_id=item.material_id,
        )

    elif item.first_image_style == "黑鲸高":
        bg = style_黑鲸高(
            im=bg,
            title=item.first_image_title,
            format=item.source_format,
            material_id=item.material_id,
            shop_name=item.shop_name,
        )

    elif item.first_image_style == "黑鲸笔刷":
        bg = Style黑鲸笔刷(
            bg=bg,
            title=item.first_image_title,
            format=item.source_format,
            material_id=item.material_id,
            format_title=item.format_title,
            shop_name=item.shop_name,
        ).main()

    elif item.first_image_style == "无样式":
        pass

    bg = bg.resize((1500, 1500), Image.Resampling.LANCZOS)
    fun_保存图片(im=bg, stem="st_" + item.first_image_num, shop_name=item.shop_name)

    return {"msg": "ok"}
