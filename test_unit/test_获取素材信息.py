from MaterialEdit import fun_创建文件夹结构
from MaterialEdit.fun_获取素材信息.fun_获取所有尺寸 import fun_获取所有尺寸
from MaterialEdit.fun_获取素材信息.fun_获取所有文件列表 import fun_获取所有文件列表
from MaterialEdit.fun_获取素材信息.fun_获取源文件数量 import fun_获取源文件数量


path_structures = fun_创建文件夹结构(root_path=r"G:\饭桶设计\1000-1999\1967")
all_file = fun_获取所有文件列表(path_structures.ma_path)
size = fun_获取所有尺寸(all_file)
num = fun_获取源文件数量(all_file)

print(size)
print(num)
