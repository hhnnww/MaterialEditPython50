from typing import Literal, Optional

from pydantic import BaseModel

_FONT_WEIGHT = Literal["light", "normal", "medium", "bold", "heavy"]
_FONT_NAME = Literal["misans", "opposans", "montserrat", "zihun", "lato", "noto", "sam"]
_COLOR = tuple[int, int, int, int]
ALIGNITEM = Literal["start", "center", "end"]


class _FontSize(BaseModel):
    width: int
    height: int


class ImageModel(BaseModel):
    path: str
    ratio: float = 0.0
    is_selected: bool = False


class _ImageItem(BaseModel):
    path: str
    width: Optional[int] = None
    height: Optional[int] = None
    ratio: float


class _FolderStructure(BaseModel):
    root_path: str
    material_path: str
    preview_path: str
    effect_path: str
    ori_img_path: str
    design_path: str


class MaterialInfo(BaseModel):
    material_path: str
    material_id: str
    material_source_file_size: str  # 789MB
    material_source_file_count: int  # 89

    material_source_format: str  # PSD AI
    material_source_format_title: str  # PSD 分层设计素材
    material_source_format_number: str  # 78个 PSD 文件

    preview_image_path: str
    preview_image_count: int
    preview_image_list: list

    effect_image_path: str
    effect_image_list: list
