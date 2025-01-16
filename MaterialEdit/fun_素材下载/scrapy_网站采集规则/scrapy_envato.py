import json
import re

from MaterialEdit.fun_素材下载.fun_session import fun_session
from MaterialEdit.fun_素材下载.model_素材格式 import MaterialModel


def fun_获取图片(img_dict: dict, reverse: bool = True):
    size_list = [
        "w2740",
        "w2038",
        "w1370",
        "w1170",
        "w1019",
        "w900",
        "w710",
        "w632",
        "w433",
    ]

    if reverse is not True:
        size_list.reverse()

    for obj in size_list:
        if img_dict.get(obj) is not None:
            return img_dict.get(obj)
    return None


def scrapy_envato(single_url: str, cookie: str):
    html = fun_session(url=single_url, cookie=cookie)

    script_list = re.findall(r"<script>([\s\S]*?)</script>", html.html)

    for script_obj in script_list:
        if "window.INITIAL_HYDRATION_DATA" in script_obj:
            # 找到原始JS本文
            ma_obj = script_obj.replace("window.INITIAL_HYDRATION_DATA=", "")
            ma_obj = ma_obj.replace(";", "")

            # 转换成JSON后 找到素材列表
            json_text = json.loads(ma_obj)
            ma_list = json_text.get("page").get("data").get("items")

            for obj in ma_list:
                ma_id = obj.get("id")
                url = f"https://elements.envato.com/items-{ma_id}"

                name = obj.get("slug")

                img = fun_获取图片(obj.get("coverImageUrls"), reverse=False) or ""

                all_list = [fun_获取图片(obj.get("coverImageUrls"))]
                for img_list in obj.get("previewImagesUrls"):
                    all_list.extend([fun_获取图片(img) for img in img_list])
                all_list = [img for img in all_list if img is not None]

                yield MaterialModel(
                    url=url,
                    img=img,
                    name=name,
                    img_list=all_list,
                    state=False,
                )
