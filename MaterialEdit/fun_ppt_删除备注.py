from pathlib import Path

from pptx import Presentation
from python_pptx_text_replacer import TextReplacer
from tqdm import tqdm


def __fun_替换本文(ppt_file: str):
    TEXT_NEED_REPLACE = ["唐峰", "芒果", "T500"]

    replacer = TextReplacer(
        ppt_file, slides="", tables=True, charts=True, textframes=True
    )
    for text in TEXT_NEED_REPLACE:
        replacer.replace_text([(text, "小夕")])

    replacer.write_presentation_to_file(ppt_file)


def __fun_删除所有备注和广告图片(ppt_file: str, ad_pic_name_list: list[str]):
    print(f"处理PPT:{ppt_file}")
    prs = Presentation(pptx=ppt_file)

    for slide in prs.slides:
        # 删除所有备注
        if slide.has_notes_slide:
            if slide.notes_slide.notes_text_frame:
                slide.notes_slide.notes_text_frame.clear()

        for shape in slide.shapes:
            try:
                if shape.shape_type:
                    # 如果是图片
                    # 查到对应的图片名字删除
                    if shape.shape_type.name == "PICTURE":
                        # if "descr=" in shape.element.xml:
                        #     print(shape.element.xml)

                        for ad_name in ad_pic_name_list:
                            if f'descr="{ad_name}"' in shape.element.xml:
                                slide.shapes._spTree.remove(shape._element)
                                print("删除广告图片")

                    # 如果是视频
                    # 直接干掉
                    elif shape.shape_type.name == "MEDIA":
                        slide.shapes._spTree.remove(shape._element)

            except:  # noqa: E722
                pass

    prs.save(file=ppt_file)


def fun_处理所有PPT(material_path: str):
    ad_pic_name_list = [f"{x}-({y})" for x in range(1, 100) for y in range(1, 100)]
    for x in range(1, 100):
        ad_pic_name_list.append(f"tm-({x})")

    for in_file in tqdm(
        list(Path(material_path).rglob("*")), ncols=100, desc="删除PPT备注"
    ):
        in_file: Path

        if in_file.is_file() and in_file.suffix.lower() in [".ppt", ".pptx"]:
            pic_path = in_file.with_suffix(".png")
            if pic_path.exists() is False:
                try:
                    __fun_删除所有备注和广告图片(
                        ppt_file=in_file.as_posix(), ad_pic_name_list=ad_pic_name_list
                    )
                    __fun_替换本文(ppt_file=in_file.as_posix())
                except:  # noqa: E722
                    pass
