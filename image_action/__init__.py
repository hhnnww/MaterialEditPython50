"""初始化模块，用于导入 ImageEdit 类。

该模块从 MaterialEdit.ImageEdit.ImageEdit 文件中导入 ImageEdit 类，
并将其添加到模块的公共接口中。
导入内容:
    - ImageEdit: 图像编辑类
"""

from image_action.image_action import ImageAction

__all__ = ["ImageAction"]
