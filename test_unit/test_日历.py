# from pprint import pprint
from PIL import Image

# from MaterialEdit.fun_文件夹操作 import MaterialPathAction
from pathlib import Path
from MaterialEdit import ImageEdit

# mk = MaterialPathAction.MakeCalenderPic(material_path=r"F:\小夕素材\10000-10999\10111\10111")
# mk.main()

for in_file in Path(r"F:\小夕素材\10000-10999\10111\10111").iterdir():
    if in_file.is_file() and in_file.suffix.lower() in [".png"]:
        eft_png = Path(r"F:\小夕素材\10000-10999\10111\效果图") / in_file.name

        ma_pil = Image.open(in_file.as_posix())
        eft_pil = Image.open(eft_png.as_posix())
        eft_pil.thumbnail((750, 999), Image.LANCZOS)

        bg = ImageEdit.fun_图片竖向拼接([eft_pil, ma_pil], 0, "center", (255, 255, 255, 255))
        bg.save((eft_png.parent / (eft_png.stem + "_all.png")).as_posix())
