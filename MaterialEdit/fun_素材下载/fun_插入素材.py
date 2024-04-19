import time
from datetime import datetime

from .fun_获取集合 import fun_获取集合
from .model_素材格式 import MaterialModel


def fun_插入素材(shop_name: str, material_site: str, material_model: MaterialModel):
    collect = fun_获取集合(shop_name=shop_name, material_site=material_site)

    material_model.img = material_model.img.replace(" ", "")
    material_model.url = material_model.url.replace(" ", "")

    if collect.count_documents({"url": material_model.url}) <= 0:
        material_model.create_date = datetime.utcnow()
        insert_id = collect.insert_one(material_model.dict()).inserted_id
        print(f"插入到数据库：{insert_id}")
        time.sleep(0.01)

    else:
        print(f"素材已经存在")
        return None
