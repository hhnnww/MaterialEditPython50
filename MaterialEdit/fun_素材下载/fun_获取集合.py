from .database import database


def fun_获取集合(shop_name: str, material_site: str):
    return database[f"{shop_name}_{material_site}"]
