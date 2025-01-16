"""MaterialEdit Package

This package provides various functionalities for handling and editing materials
image editing, folder structure creation, and more.
Modules:
- fun_AI文件处理: Contains AIFile class for handling AI files.
- fun_PS文件处理: Contains PSFile class for handling PS files.
- fun_创建文件夹结构: Provides function for creating folder structures.
- fun_制作详情: Contains functions for creating detailed information.
    - fun_制作数据图: Provides function for creating data charts.
    - fun_制作详情栏目标题: Provides function for creating detailed section titles.
    - fun_裁剪详情页图片: Provides function for cropping detailed page images.
- fun_制作首图: Contains functions for creating main images with various layouts.
- fun_图片编辑: Contains ImageEdit class for image editing.
- fun_桌面文件夹操作: Provides functions for saving images
 and clearing desktop upload folder images.
- fun_素材文件夹合并: Provides function for merging material folders.
- fun_获取素材信息: Contains function for retrieving material information.
- fun_遍历图片: Provides function for traversing images.
- get_stem_num: Provides function for getting path numbers.
- type: Contains MaterialInfo type definition.
"""

from MaterialEdit.fun_AI文件处理 import AIFile
from MaterialEdit.fun_PS文件处理 import PSFile
from MaterialEdit.fun_创建文件夹结构 import fun_创建文件夹结构
from MaterialEdit.fun_制作详情 import fun_制作详情
from MaterialEdit.fun_制作详情.fun_制作数据图 import fun_制作数据图
from MaterialEdit.fun_制作详情.fun_制作详情栏目标题 import fun_制作详情栏目标题
from MaterialEdit.fun_制作详情.fun_裁剪详情页图片 import fun_裁剪图片
from MaterialEdit.fun_制作首图 import (
    LayoutAdaptiveCrop,
    fun_layout_1_2_3,
    fun_layout_1_2_3_3,
    fun_layout_1_3,
    fun_layout_1_n,
    fun_layout_固定裁剪2,
    fun_T500首图,
    fun_黑鲸首图,
    layout_s1_n,
)
from MaterialEdit.fun_图片编辑 import ImageEdit
from MaterialEdit.fun_桌面文件夹操作 import fun_保存图片, fun_清空桌面上传文件夹图片
from MaterialEdit.fun_素材文件夹合并 import fun_素材文件夹合并
from MaterialEdit.fun_获取素材信息.fun_获取素材信息 import fun_获取素材信息
from MaterialEdit.fun_遍历图片 import fun_遍历图片
from MaterialEdit.get_stem_num import get_path_num
from MaterialEdit.type import MaterialInfo

__all__ = [
    "AIFile",
    "ImageEdit",
    "LayoutAdaptiveCrop",
    "MaterialInfo",
    "PSFile",
    "fun_T500首图",
    "fun_layout_1_2_3",
    "fun_layout_1_2_3_3",
    "fun_layout_1_3",
    "fun_layout_1_n",
    "fun_layout_固定裁剪2",
    "fun_保存图片",
    "fun_创建文件夹结构",
    "fun_制作数据图",
    "fun_制作详情",
    "fun_制作详情栏目标题",
    "fun_清空桌面上传文件夹图片",
    "fun_素材文件夹合并",
    "fun_获取素材信息",
    "fun_裁剪图片",
    "fun_遍历图片",
    "fun_黑鲸首图",
    "get_path_num",
    "layout_s1_n",
]
