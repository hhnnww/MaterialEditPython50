from pathlib import Path

import pyperclip

from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import fun_遍历指定文件


def fun_生成SKP批量导出脚本(in_path: str):
    cmd_path = Path.home() / "Desktop" / "auto_export_png.rb"

    start_args = """def save_view_to_png(file_path, img_path)
  Sketchup.open_file(file_path)
  model = Sketchup.active_model
  model.rendering_options["DisplayWatermarks"]= false
  model.rendering_options["BackgroundColor"] = Sketchup::Color.new(240, 240, 240)
  model.rendering_options["SkyColor"] = Sketchup::Color.new(240, 240, 240)
  view = model.active_view
  view.write_image(
    filename: img_path,
    width: 2000,
    height: 1300,
    antialias: true,
    transparent: false
  )
  model.close(ignore_changes=true)
end\n\n"""

    all_file = fun_遍历指定文件(folder=Path(in_path).as_posix(), suffix=[".skp"])
    for in_file in all_file:
        png_path = in_file.with_suffix(".png")
        if png_path.exists() is False:
            file_args = (
                f"save_view_to_png '{in_file.as_posix()}','{png_path.as_posix()}'\n"
            )
            start_args += file_args

    start_args += '\n\nUI.messagebox("图片已经全部导出完成!~")'

    cmd_path.write_text(start_args, encoding="utf-8")

    pyperclip.copy(f"load '{cmd_path.as_posix()}'")
