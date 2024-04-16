from PIL import Image

from MaterialEdit.fun_图片编辑.fun_图片裁剪.fun_竖图裁成横图 import fun_竖图裁成横图

# fun_横图裁成竖图(im=Image.open(r"G:\饭桶设计\1000-1999\1997\效果图\3.jpg"), width=300, height=300, position="end").show()
im = fun_竖图裁成横图(im=Image.open(r"G:\饭桶设计\1000-1999\1995\效果图\e0000_01-.jpg"), width=800, height=200, position="start")
print(im.size)
im.show()
