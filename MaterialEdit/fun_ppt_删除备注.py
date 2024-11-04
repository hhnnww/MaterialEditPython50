from pathlib import Path

from pptx import Presentation
from tqdm import tqdm

TEXT_NEED_REPLACE = [("唐峰", "小夕")]


def __replace_text(text_frame):
    for paragraph in text_frame.paragraphs:
        for run in paragraph.runs:
            for tt in TEXT_NEED_REPLACE:
                if tt[0] in run.text:
                    run.text = run.text.replace(tt[0], tt[1])


def __fun_删除所有备注(ppt_file: str):
    print(f"处理PPT:{ppt_file}")
    prs = Presentation(pptx=ppt_file)

    for slide in prs.slides:
        # 删除所有备注
        if slide.has_notes_slide:
            if slide.notes_slide.notes_text_frame:
                slide.notes_slide.notes_text_frame.clear()

        # 替换本文
        for shape in slide.shapes:
            if shape.has_text_frame:
                text_frame = shape.text_frame  # type: ignore
                __replace_text(text_frame)

            if shape.has_table:
                table = shape.table  # type: ignore
                for cell in table.iter_cells():
                    text_frame = cell.text_frame
                    __replace_text(text_frame)

            if shape.has_chart:
                text_chart = shape.chart  # type: ignore
                __replace_text(text_chart)

    prs.save(file=ppt_file)


def fun_处理所有PPT(material_path: str):
    for in_file in tqdm(
        list(Path(material_path).rglob("*")), ncols=100, desc="删除PPT备注"
    ):
        if in_file.is_file() and in_file.suffix.lower() in [".ppt", ".pptx"]:
            __fun_删除所有备注(ppt_file=in_file.as_posix())
