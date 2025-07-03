"""目录内放置广告"""

import shutil
from pathlib import Path


def _fun_子目录放广告(in_path: Path, ad_file_list: list[Path]) -> None:
    for ad_file in ad_file_list:
        new_path = in_path / ad_file.name
        if new_path.exists() is False:
            shutil.copyfile(ad_file, new_path)


def fun_目录内放置广告(material_path: str, shop_name: str) -> None:
    """目录内放置广告"""
    ma_path = Path(material_path)

    # 所有广告文件
    ad_file_list = [
        in_file
        for in_file in (
            Path(__file__).parent / "files" / "广告文件" / shop_name
        ).iterdir()
        if in_file.is_file()
    ]

    # 素材根目录放广告
    _fun_子目录放广告(in_path=ma_path, ad_file_list=ad_file_list)

    # 素材子目录放广告
    for in_path in ma_path.rglob("*"):
        if in_path.is_dir():
            _fun_子目录放广告(in_path=in_path, ad_file_list=ad_file_list)

    # 复制好评赠送
    praise_path = Path(__file__).parent / "files" / "好评赠送大礼包"

    dst_path = ma_path / f"{shop_name}_好评赠送大礼包"
    if dst_path.exists():
        dst_path.mkdir(parents=True, exist_ok=True)
    if praise_path.exists():
        shutil.copytree(
            praise_path,
            dst_path,
            dirs_exist_ok=True,
        )
