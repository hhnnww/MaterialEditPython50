from tqdm import tqdm

from .fun_构建链接列表 import fun_构建链接列表
from .scrapy_网站采集规则 import (
    scrapy_摄图,
    scrapy_包图,
    scrapy_千库,
    scrapy_享设计,
    scrapy_freepik,
    scrapy_pngtree,
    scrapy_envato,
    scrapy_千图,
)


def fun_采集单页素材(single_url: str, cookie: str, material_site: str):
    ma_list = []

    match material_site:
        case "摄图":
            ma_list = scrapy_摄图(single_url=single_url, cookie=cookie)

        case "包图":
            ma_list = scrapy_包图(single_url=single_url, cookie=cookie)

        case "千库":
            ma_list = scrapy_千库(single_url=single_url, cookie=cookie)

        case "享设计":
            ma_list = scrapy_享设计(single_url=single_url, cookie=cookie)

        case "freepik":
            ma_list = scrapy_freepik(single_url=single_url, cookie=cookie)

        case "pngtree":
            ma_list = scrapy_pngtree(single_url=single_url, cookie=cookie)

        case "envato":
            ma_list = scrapy_envato(single_url=single_url, cookie=cookie)

        case "千图":
            ma_list = scrapy_千图(single_url=single_url, cookie=cookie)

    for obj in ma_list:
        yield obj


def fun_采集(base_url: str, num: int, cookie: str, material_site: str):
    if num <= 1:
        for obj in fun_采集单页素材(single_url=base_url, cookie=cookie, material_site=material_site):
            yield obj

    else:
        for page_url in tqdm(list(fun_构建链接列表(base_url=base_url, start_num=1, end_num=num + 1)), ncols=100, desc="采集页面"):
            for obj in fun_采集单页素材(single_url=page_url, cookie=cookie, material_site=material_site):
                yield obj
