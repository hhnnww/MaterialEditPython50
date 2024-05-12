from pathlib import Path

from ..fun_获取路径数字 import fun_获取路径数字


class DownPathMoveToMaterialPath:
    def __init__(self, down_path: str, material_parent_path: str):
        self.down_path = Path(down_path)
        self.material_parent_path = Path(material_parent_path)

    def fun_获取最大目录数字(self) -> int:
        """
        自动获取素材文件夹的最大文件夹数字
        """
        all_path = [
            in_path
            for in_path in self.material_parent_path.iterdir()
            if in_path.is_dir()
        ]

        if len(all_path) > 0:
            all_path.sort(key=lambda k: fun_获取路径数字(k.stem), reverse=True)
            return int(all_path[0].stem) + 1

        return 0

    def fun_构建素材文件夹(self, in_num: int) -> Path:
        """
        给出数字,转换为str,然后构建成path
        """
        in_stem = str(in_num).rjust(4, "0")
        return self.material_parent_path / in_stem

    def main(self):
        current_num = self.fun_获取最大目录数字()
        current_path = self.fun_构建素材文件夹(current_num)

        print(current_num, current_path)
        for in_path in self.down_path.iterdir():
            if in_path.is_dir():
                if current_path.exists() is True:
                    raise IndexError("素材目标文件夹存在")
                in_path.rename(current_path)

                print(in_path, "->", current_path)
                current_num += 1
                current_path = self.fun_构建素材文件夹(in_num=current_num)
