"""制作淘宝详情."""

from pathlib import Path

from pydantic import BaseModel

from MaterialEdit import (
    fun_保存图片,
    fun_制作数据图,
    fun_制作详情栏目标题,
    fun_清空桌面上传文件夹图片,
    fun_裁剪图片,
    fun_遍历图片,
)
from MaterialEdit.fun_图片编辑.fun_图片拼接.fun_图片竖向拼接 import fun_图片竖向拼接
from MaterialEdit.router_制作详情2.class_制作详情 import ClassMakeXQ2
from MaterialEdit.type import ALIGNITEM


class MakeProductImageRequestModel(BaseModel):
    shop_name: str
    material_path: str
    preview_image_path: str
    effect_image_path: str

    # 数据图
    material_id: str
    material_source_file_size: str
    material_source_format_title: str
    material_source_format_number: str

    # 制作详情
    oneline_number: int
    oneline_ratio: float
    has_preview_image: int
    has_effect_image: int

    preview_image_sort: int
    preview_used_number: int
    preview_has_material_info: int
    preview_image_count: int

    effect_has_watermark: bool

    crop_position: ALIGNITEM
    xq_width: int
    image_name_has_material_id: bool = False

    clear_upload_path: bool = True
    has_water: int


def fun_制作详情2(item: MakeProductImageRequestModel) -> None:  # noqa: C901, PLR0912
    """制作详情"""
    if item.clear_upload_path:
        fun_清空桌面上传文件夹图片("xq")

    num = 1
    # 制作数据图
    data_header = fun_制作详情栏目标题(
        title="素材信息",
        desc="Material Info " + item.shop_name,
    )

    data_list = [
        ("素材ID", item.material_id),
        ("素材大小", item.material_source_file_size),
        ("素材格式", item.material_source_format_title),
        ("素材数量", item.material_source_format_number),
        ("* 发货方式", "本店仅限百度网盘链接发货，不支持其他任何发送方式。"),
        (
            "* 非图片",
            "本店素材并非图片，为专业设计师使用的设计源文件，非设计师请勿购买。",
        ),
    ]

    if item.shop_name == "泡泡素材":
        data_list.append(("* 无模特图", "本店素材均不包含模特图效果图。"))

    data_pil = fun_制作数据图(data_list)
    data_im = fun_图片竖向拼接(
        [data_header, data_pil],
        spacing=0,
        align_item="center",
        background_color=(255, 255, 255, 255),
    )

    if item.image_name_has_material_id is True:
        fun_保存图片(
            im=data_im,
            stem=f"xq_{num}",
            shop_name=item.shop_name,
            material_id=item.material_id,
        )
    else:
        fun_保存图片(data_im, f"xq_{num}", shop_name=item.shop_name)
    num += 1

    # ---------------- 制作效果图 ----------------

    if item.has_effect_image and Path(item.effect_image_path).exists() is True:
        image_list = [
            obj
            for obj in fun_遍历图片(
                folder=item.effect_image_path,
                used_image_number=0,
                image_sort=True,
            )
            if "_thumb" not in Path(obj).stem
        ]

        if len(image_list) > 0:
            header_pil = fun_制作详情栏目标题(
                title="素材效果图",
                desc="* 此图片素材内不提供",
            )

            effect_image = ClassMakeXQ2(
                image_list=[Path(image) for image in image_list],
                col=item.oneline_number,
                shop_name=item.shop_name,
                has_name=False,
                use_pic=len(image_list),
                pic_sort=True,
                material_path=Path(item.material_path),
                has_water=item.has_water == 1,
                oneline_ratio=item.oneline_ratio,
                effect_has_watermark=item.effect_has_watermark,
            ).main()

            data_im = fun_图片竖向拼接(
                [header_pil, effect_image],
                spacing=0,
                align_item="center",
                background_color=(255, 255, 255, 255),
            )

            for im in fun_裁剪图片(im=data_im):
                if item.image_name_has_material_id is True:
                    fun_保存图片(
                        im=im,
                        stem=f"xq_{num}",
                        material_id=item.material_id,
                        shop_name=item.shop_name,
                    )
                else:
                    fun_保存图片(im=im, stem=f"xq_{num}", shop_name=item.shop_name)
                num += 1

    # 制作预览图
    if item.has_preview_image == 1 and Path(item.preview_image_path).exists() is True:
        image_list = [
            obj
            for obj in fun_遍历图片(
                folder=item.preview_image_path,
                used_image_number=item.preview_used_number,
                image_sort=item.preview_image_sort == 1,
            )
            if "_thumb" not in Path(obj).stem
        ]
        if len(image_list) > 0:
            header_pil = fun_制作详情栏目标题(
                title="素材预览图",
                desc="* 预览图与源文件对应",
            )

            sort = item.preview_image_sort == 1
            has_name = item.preview_has_material_info == 1

            preview_image = ClassMakeXQ2(
                image_list=[Path(image) for image in image_list],
                col=item.oneline_number,
                shop_name=item.shop_name,
                has_name=has_name,
                use_pic=item.preview_used_number,
                pic_sort=sort,
                material_path=Path(item.material_path),
                has_water=item.has_water == 1,
                oneline_ratio=item.oneline_ratio,
                effect_has_watermark=item.effect_has_watermark,
            ).main()

            data_im = fun_图片竖向拼接(
                image_list=[header_pil, preview_image],
                spacing=0,
                align_item="center",
                background_color=(255, 255, 255, 255),
            )
            for im in fun_裁剪图片(im=data_im):
                if item.image_name_has_material_id is True:
                    fun_保存图片(
                        im=im,
                        stem=f"xq_{num}",
                        material_id=item.material_id,
                        shop_name=item.shop_name,
                    )
                else:
                    fun_保存图片(im=im, stem=f"xq_{num}", shop_name=item.shop_name)
                num += 1
