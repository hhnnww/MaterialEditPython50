from pathlib import Path

import pyperclip

from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob


def fun_生成SKP批量导出脚本(in_path: str):
    start_args = """def save_view_to_png(file_path, img_path)
  Sketchup.open_file(file_path)
  model = Sketchup.active_model
  model.rendering_options["DisplayWatermarks"]= false
  model.rendering_options["BackgroundColor"] = Sketchup::Color.new(240, 240, 240)
  model.rendering_options["SkyColor"] = Sketchup::Color.new(240, 240, 240)
  model.rendering_options["EdgeColorMode"] = 1
  model.rendering_options["DisplayFog"] = false
  
  # 隐藏坐标线
  model.rendering_options["DisplaySketchAxes"] = false

  # 隐藏背景线
  model.rendering_options["DrawBackEdges"] = false
  
  # 设置为细线 
  model.rendering_options["DrawDepthQue"] = false

  # 隐藏地面
  model.rendering_options["DrawGround"] = false
  
  # 隐藏辅助线 DrawHidden
  model.rendering_options["DrawHidden"] = false

  # 隐藏辅助线 DrawHiddenGeometry
  model.rendering_options["DrawHiddenGeometry"] = false

  # 地平线
  model.rendering_options["DrawHorizon"] = false

  # 绘制线条端点
  model.rendering_options["DrawLineEnds"] = false

  # 隐藏轮廓线
  model.rendering_options["DrawSilhouettes"] = false

  # 隐藏边线
  model.rendering_options["EdgeDisplayMode"] = false

  # 隐藏所有阴影
  model.shadow_info['DisplayShadows'] = false

  view = model.active_view
  # view.zoom_extents
  large_size = 3000
  radio =  view.vpwidth.to_f / view.vpheight.to_f
  height = large_size / radio

  options = {
  :filename => img_path,
  :width => large_size,
  :height => height.to_i,
  :antialias => true,
  :compression => 0.9,
  :transparent => false
  }

  view.write_image(
    options
  )

    model.close(ignore_changes=true)
end
\n\n\n
"""

    all_file = rglob(folder=Path(in_path).as_posix(), suffix=[".skp"])
    for in_file in all_file:
        png_path = in_file.with_suffix(".png")
        if png_path.exists() is False:
            file_args = f"save_view_to_png '{in_file.as_posix()}','{png_path.as_posix()}'\n"
            start_args += file_args

    start_args += '\n\nUI.messagebox("图片已经全部导出完成!~")'
    pyperclip.copy(start_args)
