import re


class Cla_ImageObj:
    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url

    @property
    def fun_图片数字(self) -> int:
        num = re.findall(r"\d", self.name)
        return int("".join(num))

    @property
    def fun_图片ID(self) -> int:
        return int(self.name[:4])

    def __str__(self) -> str:
        return f"name:{self.name}\turl:{self.url}"


if __name__ == "__main__":
    obj = Cla_ImageObj("2088-xq_2.jpg", "laksdjflakjsldkfa")
    print(obj.fun_图片ID, obj.fun_图片数字)
