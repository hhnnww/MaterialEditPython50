from .fun_获取集合 import fun_获取集合


def fun_获取素材(shop_name: str, material_site: str, page: int):
    one_page_count = 60

    collect = fun_获取集合(shop_name=shop_name, material_site=material_site)
    ma_list = list(collect.find({"state": False}).skip((page - 1) * one_page_count).limit(one_page_count))

    count = collect.count_documents({"state": False})

    for obj in ma_list:
        obj["_id"] = str(obj["_id"])

    return ma_list, count
