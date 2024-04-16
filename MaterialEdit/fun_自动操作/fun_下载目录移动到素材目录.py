from pathlib import Path

from ..fun_获取路径数字 import fun_获取路径数字


class DownPathMoveToMaterialPath:
    def __init__(self, down_path: str, material_parent_path: str):
        self.down_path = Path(down_path)
        self.material_parent_path = Path(material_parent_path)

    def fun_获取最大目录数字(self) -> int:
        all_path = [in_path for in_path in self.material_parent_path.iterdir() if in_path.is_dir()]
        all_path.sort(key=lambda k: fun_获取路径数字(k.stem), reverse=True)
        return int(all_path[0].stem) + 1

    def main(self):
        current_num = self.fun_获取最大目录数字()

        current_stem = str(current_num)
        if len(current_stem) < 4:
            current_stem = "0" + current_stem

        current_path = self.material_parent_path / current_stem

        print(current_num, current_path)
        for in_path in self.down_path.iterdir():
            if in_path.is_dir():
                in_path.rename(current_path)
                print(in_path, "->", current_path)
                current_num += 1

                current_stem = str(current_num)
                if len(current_stem) < 4:
                    current_stem = "0" + current_stem

                current_path = self.material_parent_path / str(current_stem)
