from MaterialEdit import fun_制作详情, fun_遍历图片

im = fun_制作详情(
    image_path_list=fun_遍历图片(r"G:\饭桶设计\2000-2999\2715\预览图", 6, True),
    line_number=3,
    max_line_ratio=1.5,
    contains_info=True,
    material_path=r"G:\饭桶设计\2000-2999\2666\2666",
    xq_width=1500,
    crop_position="center",
)

im.show()
