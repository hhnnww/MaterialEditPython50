"""文件夹操作."""

import subprocess
from uuid import uuid4

import pythoncom
from win32com.client import Dispatch

from fun_素材文件夹.export_image import ExportImage
from fun_素材文件夹.fun_AI文件处理.al_file import AiFile
from fun_素材文件夹.material_base_func import MaterialType
from fun_素材文件夹.root_path import RootFolder


class MaterialAction(RootFolder):
    def fun_删除素材图图片边框(self) -> None:
        """删除素材图图片边框."""
        for material in self.mateiral_path.all_material:
            for image in material.material_images:
                image.fun_图片删除边框()

    def fun_打开没有预览图的AI文件(self) -> None:
        """打开没有预览图的AI文件."""
        ExportImage.fun_打开AI文件(
            path_list=[
                material.path
                for material in self.mateiral_path.all_material
                if material.path.suffix.lower() in [".ai", ".eps"] and material.has_material_image is False
            ],
        )

    def fun_打开没有预览图的PSD文件(self) -> None:
        """打开没有预览图的PSD文件."""
        ExportImage.fun_打开PSD文件(
            path_list=[
                material.path
                for material in self.mateiral_path.all_material
                if material.path.suffix.lower() in [".psd", ".psb"] and material.has_material_image is False
            ],
        )

    def fun_打开没有预览图的PPT文件(self) -> None:
        """打开没有预览图的PPT文件."""
        pythoncom.CoInitialize()
        app = Dispatch("PowerPoint.Application")
        for num, material in enumerate(
            [
                infile
                for infile in self.mateiral_path.all_material
                if infile.path.suffix.lower() in [".ppt", ".pptx"] and infile.has_material_image is False
            ],
        ):
            MaterialType.log(f"打开没有预览图的PPT文件{material.path.as_posix()}")
            app.Open(material.path.as_posix())
            if num == self.max_open_file:
                return
        pythoncom.CoUninitialize()

    def fun_素材源文件对应的素材图重命名(self) -> None:
        """所有素材文件对应的所有素材图重命名."""
        for material in self.mateiral_path.all_material:
            material.fun_修改素材源文件对应的素材图名称(
                material_path=self.mateiral_path.path,
                preview_path=self.preview_path.path,
            )

    def fun_复制素材图到预览图(self) -> None:
        """把素材文件夹内的素材图复制到预览图."""
        if self.preview_path.path.exists() is not True:
            self.preview_path.path.mkdir()

        # 复制到预览图
        for material in self.mateiral_path.all_material:
            for image in material.material_images:
                image.fun_复制素材图到预览图(material_path=self.mateiral_path.path, preview_path=self.preview_path.path)

    def fun_移动到根目录(self) -> None:
        """素材文件夹内所有文件移动到根目录."""
        MaterialType.fun_移动到根目录(folder=self.mateiral_path.path)

    def fun_删除压缩文件(self) -> None:
        """删除所有压缩文件."""
        for infile in self.mateiral_path.path.iterdir():
            if infile.is_file() and infile.suffix.lower() in MaterialType.zip_suffix:
                infile.unlink()

    def fun_文件重命名(self, shop_name: str, start_num: int = 1) -> None:
        """重命名所有素材和源文件."""
        uuid_stem = str(uuid4())
        # 先改成UUID文件名
        for num, material in enumerate(self.mateiral_path.all_material):
            new_stem = f"{uuid_stem}({num})"
            material.fun_修改素材源文件以及素材图和预览图名称(
                new_stem=new_stem,
                material_path=self.mateiral_path.path,
                preview_path=self.preview_path.path,
            )

        # 再改成店铺名
        for num, material in enumerate(self.mateiral_path.all_material):
            new_stem = f"{shop_name}({num+start_num})"
            material.fun_修改素材源文件以及素材图和预览图名称(
                new_stem=new_stem,
                material_path=self.mateiral_path.path,
                preview_path=self.preview_path.path,
            )

    def fun_打开素材文件夹(self) -> None:
        """打开素材图."""
        subprocess.Popen(args=["explorer.exe", self.mateiral_path.path.as_posix().replace("/", "\\")], shell=True)

    def fun_EPS转AI文件(self) -> None:
        """EPS文件转成AI文件."""
        pythoncom.CoInitialize()
        app = Dispatch("Illustrator.Application")
        for material in [
            material for material in self.mateiral_path.all_material if material.path.suffix.lower() in [".eps"]
        ]:
            doc = app.Open(material.path.as_posix())
            doc.SaveAs(material.path.with_suffix(".ai"))
            doc.Close(2)
            material.path.unlink()
        pythoncom.CoUninitialize()

    def fun_删除素材文件夹内所有图片(self) -> None:
        """删除素材文件夹内的所有素材图."""
        [
            infile.unlink()
            for infile in self.mateiral_path.path.rglob("*")
            if infile.is_file() and infile.suffix.lower() in MaterialType.image_suffix
        ]

    def fun_子目录移动到根目录(self) -> None:
        """所有子目录移动到根."""
        [subpath.fun_子目录文件移动到根目录() for subpath in self.mateiral_path.all_sub_path]

    def fun_子目录重命名(self, shop_name: str, start_num: int = 1) -> None:
        """所有子目录重命名."""
        uuid_stem = str(uuid4())
        for num, subpath in enumerate(self.mateiral_path.all_sub_path):
            new_stem = f"{uuid_stem}({num})"
            subpath.fun_子目录重命名(new_stem=new_stem)

        for num, subpath in enumerate(self.mateiral_path.all_sub_path):
            new_stem = f"{shop_name}({num+start_num})"
            subpath.fun_子目录重命名(new_stem=new_stem)

    def fun_子目录AI文件重命名(self) -> None:
        """把子目录内的AI文件重命名."""
        [subpath.fun_子目录AI重命名() for subpath in self.mateiral_path.all_sub_path]

    def fun_子目录AI文件夹重构(self) -> None:
        """所有子目录重构."""
        [subpath.fun_AI文件夹重构() for subpath in self.mateiral_path.all_sub_path]

    def fun_删除广告文件(self) -> None:
        """删除素材文件夹内的广告文件."""
        for infile in self.mateiral_path.path.rglob("*"):
            if (infile.suffix.lower() in MaterialType.ad_suffix or infile.name in [".DS_Store"]) and infile.is_file():
                infile.unlink()

    def fun_素材源文件素材图预览图移动到子目录(self) -> None:
        """素材源文件素材图预览图移动到子目录."""
        for material in self.mateiral_path.all_material:
            material.fun_移动到子目录(material_path=self.mateiral_path.path, preview_path=self.preview_path.path)

    def fun_PSD导出预览图(self) -> None:
        """PSD导出预览图."""
        ExportImage.fun_PSD文件导出PNG(
            path_list=[
                material.path
                for material in self.mateiral_path.all_material
                if material.path.suffix.lower() in [".psd", ".psb"] and material.has_material_image is False
            ],
        )

    def fun_AI导出预览图(self) -> None:
        """AI文件导出PNG."""
        [
            AiFile(material.path).main()
            for material in self.mateiral_path.all_material
            if material.path.suffix.lower() in [".ai", ".eps"] and material.has_material_image is False
        ]


if __name__ == "__main__":
    action = MaterialAction(path=r"F:\小夕素材\11000-11999\11014")
    action.fun_AI导出预览图()
