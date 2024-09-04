from pathlib import Path
from typing import Optional

from ...type import _FONT_NAME, _FONT_WEIGHT


def fun_获取字体(
    font_name: _FONT_NAME,
    font_weight: _FONT_WEIGHT,
) -> Optional[str]:
    font_root_path = Path(__file__).parent / "font"
    font_dict = {
        "misans": {
            "light": "MiSans-Light.ttf",
            "normal": "MiSans-Normal.ttf",
            "bold": "MiSans-Bold.ttf",
            "heavy": "MiSans-Heavy.ttf",
        },
        "opposans": {
            "light": "OPPOSans-L.ttf",
            "normal": "OPPOSans-R.ttf",
            "bold": "OPPOSans-B.ttf",
            "heavy": "OPPOSans-H.ttf",
        },
        "montserrat": {
            "light": "montserrat-latin-300-normal.ttf",
            "normal": "montserrat-latin-400-normal.ttf",
            "bold": "montserrat-latin-600-normal.ttf",
            "heavy": "montserrat-latin-700-normal.ttf",
        },
        "zihun": {
            "light": "字魂3号-英雄黑体.ttf",
            "normal": "字魂3号-英雄黑体.ttf",
            "bold": "字魂3号-英雄黑体.ttf",
            "heavy": "字魂3号-英雄黑体.ttf",
        },
        "lato": {
            "light": "lato-latin-300-normal.ttf",
            "normal": "lato-latin-400-normal.ttf",
            "bold": "lato-latin-700-normal.ttf",
            "heavy": "lato-latin-900-normal.ttf",
        },
        "noto": {
            "light": "light.otf",
            "normal": "regular.otf",
            "bold": "bold.otf",
            "heavy": "black.otf",
        },
        "sam": {
            "light": "samsungsharpsans.otf",
            "normal": "samsungsharpsans-medium.otf",
            "bold": "samsungsharpsans-bold.otf",
            "heavy": "samsungsharpsans-bold.otf",
        },
    }

    font_name_obj = font_dict.get(font_name)
    if font_name_obj is not None:
        font_name_weight_obj = font_name_obj.get(font_weight)
        if font_name_weight_obj is not None:
            font_path: Path = font_root_path / font_name / font_name_weight_obj
            return font_path.as_posix()

    return None
