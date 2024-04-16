from MaterialEdit.fun_图片编辑 import ImageEdit

ImageEdit.fun_制作多行本文(
    "前面的示例在输出的中间混合了嵌入了tab和space，所以输出的结果不尽人意。使用从示例文本的所有行中删除公共空白前缀会产生更好的结果，并允许直接从Python代码中使用docstring或嵌入的多行字符串，同时删除代码本身的格式。",
    50,
    30,
    "opposans",
    "montserrat",
    "normal",
    40,
    (255, 255, 255, 255),
    (0, 0, 0, 255),
    en_size_expand_ratio=1,
).show()
