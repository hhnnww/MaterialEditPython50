from pathlib import Path

MATERIAL_SOURCE_SUFFIX = [
    ".psd",
    ".ai",
    ".otf",
    ".ttf",
    ".ttc",
    ".psb",
    ".eps",
    ".ppt",
    ".pptx",
    ".procreate",
    ".brushset",
    ".abr",
    ".cdr",
    ".skp",
]

IMAGE_SUFFIX = [".jpg", ".png", ".jpeg", ".gif"]

FONT_COLOR = (90, 90, 120, 255)

HOME_UPDATE_FOLDER = Path.home() / "Desktop" / "UPLOAD"

FIRST_IMAGE_RATIO = 10
FIRST_IMAGE_BORDER_COLOR = (240, 240, 240, 255)

AD_SUFFIX = [
    ".html",
    ".exe",
    ".url",
    ".doc",
    ".txt",
    ".mp4",
    ".pdf",
    ".htm",
    ".ntim",
    ".otf",
    ".ttf",
    ".ttc",
    ".lnk",
    ".skb",
]


OUT_PATH = Path().home() / "desktop" / "OUT_PATH"
if OUT_PATH.exists() is False:
    OUT_PATH.mkdir()
