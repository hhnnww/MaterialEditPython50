import shutil
from pathlib import Path

from .fun_PPT导出图片 import PPTFile
from .fun_图片组合 import PPTPICMerge


class PPTEdit:
    def __init__(self, ppt_path: Path, ppt_export_path: Path, effect_path: str):
        self.ppt_path = ppt_path
        self.ppt_export_path = ppt_export_path
        self.effect_path = Path(effect_path)

        if self.effect_path.exists() is not True:
            self.effect_path.mkdir()

    def main(self):
        ppt_export = PPTFile(self.ppt_path, self.ppt_export_path)
        if ppt_export.fun_导出PNG() == "ok":
            ppt_dir = ppt_export.ppt_dir

            # for in_file in ppt_dir.iterdir():
            #     if in_file.is_file():
            #         effect_image = self.effect_path / f"{str(uuid4())}.png"
            #         shutil.copy(in_file, effect_image)
            #         break

            bg = PPTPICMerge(ppt_dir)
            bg = bg.main()

            ppt_png = self.ppt_path.with_suffix(".png")
            bg.save(ppt_png.as_posix())

            bg.save(self.effect_path / f'{self.ppt_path.with_suffix('.png').name}')

            for in_file in ppt_dir.iterdir():
                if in_file.is_file():
                    new_stem = "99" + in_file.stem
                    if in_file.with_stem(new_stem).exists() is False:
                        in_file.rename(in_file.with_stem(new_stem))

            shutil.rmtree(ppt_dir)
