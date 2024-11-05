import json
from pathlib import Path
from random import randint

from pydantic import BaseModel
from pypinyin import lazy_pinyin


class ChengyuOBJ(BaseModel):
    word: str
    py: str


class Class_随机获取一个成语:
    @staticmethod
    def fun_成语文件() -> ChengyuOBJ:
        cy_path = Path(__file__).parent / "成语文件" / "data" / "idiom.json"
        with open(cy_path.as_posix(), mode="r", encoding="utf-8") as chengyu:
            cy_json = json.loads(chengyu.read())

            cy = cy_json[randint(0, len(cy_json))]
            while len(cy.get("word")) > 5 or len(cy.get("word")) < 3:
                cy = cy_json[randint(0, len(cy_json))]

            return ChengyuOBJ(
                word=cy.get("word"), py=" ".join(lazy_pinyin(cy.get("word")))
            )


if __name__ == "__main__":
    cyobj = Class_随机获取一个成语
    print(cyobj.fun_成语文件())
