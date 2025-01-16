"""module provides functionality to download images from Envato.

and save them to a specified directory.

Functions:
    fun_envato_图片下载(obj: dict, down_path: str | Path) -> None:
        Downloads images from Envato and saves them to the specified path.
Dependencies:
    - logging
    - pathlib.Path
    - requests_html.HTMLSession
    - tqdm.tqdm
"""

from __future__ import annotations

import logging
from pathlib import Path

from requests_html import HTMLSession
from tqdm import tqdm


def fun_envato_图片下载(obj: dict, down_path: str | Path) -> None:
    """下载envato图片并保存到指定路径。

    参数:
        obj (dict): 包含图片信息的字典对象，必须包含键 "name" 和 "img_list"。
        down_path (str | Path): 图片保存的根目录路径。
    """
    down_path = Path(down_path)
    if down_path.exists() is False:
        down_path.mkdir()
    img_dir = down_path / obj.get("name", "")

    num = 1
    while img_dir.exists() is True:
        img_dir = down_path / f"{obj.get('name')}_{num}"
        num += 1

    if img_dir.exists() is False:
        img_dir.mkdir()

    num = 1
    for img in tqdm(obj.get("img_list"), ncols=100, desc="下载envato图片"):
        img_file = img_dir / (str(num) + ".png")
        msg = f"下载图片: {img_file.name}"
        logging.info(msg)
        with HTMLSession() as session:
            content = session.get("https://proxy.yumiwudesign.com/?path=" + img).content
            img_file.write_bytes(content)
            num += 1
