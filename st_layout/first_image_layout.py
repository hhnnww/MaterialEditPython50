"""固定裁剪布局"""

from st_layout.__layout_固定裁剪 import Layout固定裁剪


class FirstImageLayout(Layout固定裁剪):
    pass


if __name__ == "__main__":
    from pathlib import Path

    image_list = list(Path(r"F:\小夕素材\11000-11999\11229\11229").glob("*.jpg"))
    gd = FirstImageLayout(image_list)
    gd.bg_color = "#fff"
    gd.radio = 0
    gd.col = 3
    gd.spacing = 0
    gd.has_out_spacing = True
    gd.fun_图片固定裁剪().show()
