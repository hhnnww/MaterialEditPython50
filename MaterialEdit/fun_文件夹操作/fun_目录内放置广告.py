import shutil
from pathlib import Path


def _fun_子目录放广告(in_path: Path, ad_file_list: list[Path]):
    for ad_file in ad_file_list:
        new_path = in_path / ad_file.name
        if new_path.exists() is False:
            shutil.copyfile(ad_file, new_path)


def fun_目录内放置广告(material_path: str, shop_name: str):
    ma_path = Path(material_path)

    # 所有广告文件
    ad_file_list = []
    for in_file in (Path(__file__).parent / "files" / "广告文件" / shop_name).iterdir():
        if in_file.is_file():
            ad_file_list.append(in_file)

    # 素材根目录放广告
    _fun_子目录放广告(in_path=ma_path, ad_file_list=ad_file_list)

    # 素材子目录放广告
    for in_path in ma_path.rglob("*"):
        if in_path.is_dir():
            _fun_子目录放广告(in_path=in_path, ad_file_list=ad_file_list)
