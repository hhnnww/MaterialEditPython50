from pathlib import Path
from typing import Iterator


def fun_构建链接列表(base_url: str, start_num: int, end_num: int) -> Iterator[str]:
    # 如果是享设计
    if "https://www.design006.com/" in base_url:
        for page in 享设计获取URL列表(url=base_url, max_num=end_num):
            yield page

    # 如果是其他素材网站
    else:
        for x in range(start_num, end_num):
            yield base_url.replace("*", str(x))


def 享设计获取URL列表(url: str, max_num: int) -> Iterator[str]:
    # 如果是作者页面
    if "homepage" in url:
        user_id = url.split("-")[1]

        for x in range(1, max_num):
            yield f"https://www.design006.com/Home/Index/get_homepage/p/{x}/user_id/{user_id}/option_most/2"

    # 如果是常规页面
    else:
        url_parts = Path(url).name.split("-")

        for x in range(1, max_num):
            yield f"https://www.design006.com/Home/Index/get_data_index2/p/{x}/keywords/{url_parts[1]}/color_id/{url_parts[2]}/work_type_id/{url_parts[3]}/option_most/{url_parts[4]}/is_free/{url_parts[5]}/typesetting/{url_parts[7]}/sort/{url_parts[8]}/format/{url_parts[9]}"
