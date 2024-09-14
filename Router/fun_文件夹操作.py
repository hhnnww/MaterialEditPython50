import os
import shutil
from pathlib import Path
from pprint import pprint

import pythoncom
from pydantic import BaseModel
from tqdm import tqdm
from win10toast import ToastNotifier  # type: ignore
from win32com.client import Dispatch

from MaterialEdit import AIFile, PPTEdit, PSFile
from MaterialEdit.fun_PS文件处理.fun_对比所有导出的图片 import fun_所有广告图片
from MaterialEdit.fun_文件夹操作 import ImageCopyToPreview
from MaterialEdit.fun_文件夹操作.fun_AI文件重命名 import fun_ai文件重命名
from MaterialEdit.fun_文件夹操作.fun_享设计文件夹重构 import fun_享设计文件夹重构
from MaterialEdit.fun_文件夹操作.fun_删除AI对应的PNG图片 import fun_删除AI对应的PNG文件
from MaterialEdit.fun_文件夹操作.fun_删除EPS文件 import fun_删除EPS文件
from MaterialEdit.fun_文件夹操作.fun_删除图片边框 import fun_删除图片边框
from MaterialEdit.fun_文件夹操作.fun_删除广告文件 import fun_删除广告文件
from MaterialEdit.fun_文件夹操作.fun_删除文件夹 import fun_删除文件夹
from MaterialEdit.fun_文件夹操作.fun_删除素材文件夹所有图片 import (
    fun_删除素材文件夹所有图片,
)
from MaterialEdit.fun_文件夹操作.fun_制作享设计大图 import fun_享设计制作预览图
from MaterialEdit.fun_文件夹操作.fun_图片添加白色背景 import fun_图片添加白色背景
from MaterialEdit.fun_文件夹操作.fun_子目录psd重命名 import fun_子目录PSD重命名
from MaterialEdit.fun_文件夹操作.fun_子目录图片重命名 import fun_子目录图片重命名
from MaterialEdit.fun_文件夹操作.fun_打开所有子文件夹 import fun_打开所有子文件夹
from MaterialEdit.fun_文件夹操作.fun_按数字分类 import fun_按数字分类
from MaterialEdit.fun_文件夹操作.fun_文件夹内文件夹重命名 import (
    fun_文件夹内文件夹重命名,
)
from MaterialEdit.fun_文件夹操作.fun_文件夹初始化 import fun_文件夹初始化
from MaterialEdit.fun_文件夹操作.fun_文件重命名 import fun_文件重命名
from MaterialEdit.fun_文件夹操作.fun_移动到效果图 import fun_移动到效果图
from MaterialEdit.fun_文件夹操作.fun_移动到根目录 import fun_移动到根目录
from MaterialEdit.fun_文件夹操作.fun_素材图水印 import fun_素材图水印
from MaterialEdit.fun_文件夹操作.fun_解压ZIP import fun_解压ZIP
from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import fun_遍历指定文件
from MaterialEdit.setting import HOME_UPDATE_FOLDER, OUT_PATH

toaster = ToastNotifier()


def fun_通知(msg: str):
    toaster.show_toast(title="素材编辑程序", msg=msg, threaded=True, duration=2)


class RequestMaterialPathActionModel(BaseModel):
    action: str
    shop_name: str
    root_path: str

    file_start_stem: str
    path_start_stem: str


def fun_material_path_action(item: RequestMaterialPathActionModel):
    pprint(item)

    material_structure = fun_文件夹初始化(root_path=item.root_path)

    match item.action:
        case "打开所有子文件夹":
            fun_打开所有子文件夹(material_path=material_structure.material_path)

        case "打开素材文件夹":
            os.startfile(material_structure.material_path)

        case "打开预览图文件夹":
            os.startfile(material_structure.preview_path)

        case "打开效果图文件夹":
            if Path(material_structure.effect_path) is True:
                os.startfile(material_structure.effect_path)

        case "打开桌面上传文件夹":
            os.startfile(HOME_UPDATE_FOLDER.as_posix())

        case "删除效果图":
            fun_删除文件夹(folder=material_structure.effect_path)

        case "删除预览图":
            fun_删除文件夹(folder=material_structure.preview_path)

        case "解压ZIP":
            for in_file in tqdm(
                fun_遍历指定文件(
                    folder=material_structure.material_path, suffix=[".zip"]
                ),
                ncols=100,
                desc="解压ZIP\t",
            ):
                fun_解压ZIP(file_path=in_file)

        case "移动到根目录":
            fun_移动到根目录(folder=material_structure.material_path)
            if Path(material_structure.preview_path).exists() is True:
                fun_移动到根目录(folder=material_structure.preview_path)

        case "删除广告文件":
            fun_删除广告文件(folder=material_structure.material_path)

        case "文件重命名":
            fun_文件重命名(
                folder=material_structure.material_path,
                preview_path=material_structure.preview_path,
                shop_name=item.shop_name,
                num=int(item.file_start_stem),
            )

        case "删除素材文件夹内所有图片":
            fun_删除素材文件夹所有图片(folder=material_structure.material_path)

        case "复制图片到预览图":
            ac = ImageCopyToPreview(
                folder_path=material_structure.material_path,
                preview_path=material_structure.preview_path,
            )
            ac.main()

        case "移动到效果图":
            fun_移动到效果图(
                material_path=material_structure.material_path,
                effect_path=material_structure.effect_path,
            )

        case "素材图水印":
            fun_素材图水印(
                material_path=material_structure.material_path, shop_name=item.shop_name
            )

        case "按数字分类":
            fun_按数字分类(material_path=material_structure.material_path)
            fun_按数字分类(material_path=material_structure.preview_path)

        case "AI-导出图片":
            all_file = []
            all_file.extend(
                fun_遍历指定文件(material_structure.material_path, [".ai", ".eps"])
            )

            pythoncom.CoInitialize()  # type: ignore
            app = Dispatch("Illustrator.Application")
            for in_file in tqdm(all_file, ncols=100, desc="处理AI文件"):
                png_path = in_file.with_suffix(".png")
                png_state = png_path.exists()

                if png_state is False:
                    all_png = [
                        in_png.stem
                        for in_png in fun_遍历指定文件(
                            material_structure.material_path, [".png"]
                        )
                    ]
                    for in_png in all_png:
                        if in_file.stem in in_png:
                            png_state = True

                if png_state is False:
                    AIFile(in_file.as_posix(), app).fun_导出PNG()

            app.Quit()

            pythoncom.CoUninitialize()  # type: ignore

            for in_file in Path(material_structure.material_path).rglob("*"):
                if in_file.is_dir() and in_file.name == "3000w":
                    shutil.rmtree(in_file.as_posix())

        case "PSD-删除广告-导出图片-添加广告":
            # 获取所有PSD
            all_file = []
            all_file.extend(
                fun_遍历指定文件(material_structure.material_path, [".psd", ".psb"])
            )

            # 清空OUT_PATH
            for in_file in OUT_PATH.iterdir():
                if in_file.is_file():
                    in_file.unlink()
                else:
                    shutil.rmtree(in_file.as_posix())

            pythoncom.CoInitialize()  # type: ignore
            ad_pic_list = fun_所有广告图片()
            for in_file in tqdm(all_file, ncols=100, desc="删除广告导出图片\t"):
                png_path = in_file.with_suffix(".png")
                if png_path.exists() is False:
                    # 如果是4KB的PSD不处理
                    if in_file.stat().st_size == 4096:
                        print("错误PSD文件", in_file)
                        continue

                    # 大小判断，超大的不处理
                    size = in_file.stat().st_size / 1024 / 1024
                    if size > 300:
                        print(f"{in_file}:\t文件尺寸:\t{size},太大，不处理。")
                        continue

                    PSFile(
                        ps_path=in_file.as_posix(),
                        tb_name=item.shop_name,
                        ad_pic_list=ad_pic_list,
                    ).run_删除广告导出PNG()

            pythoncom.CoUninitialize()  # type: ignore

        case "PSD-导出图片-添加广告":
            # 获取所有PSD
            all_file = []
            all_file.extend(
                fun_遍历指定文件(material_structure.material_path, [".psd", ".psb"])
            )

            pythoncom.CoInitialize()  # type: ignore
            for in_file in tqdm(all_file, ncols=100, desc="导出图片，添加广告\t"):
                png_path = in_file.with_suffix(".png")
                if png_path.exists() is False:
                    if in_file.stat().st_size == 4096:
                        print("错误PSD文件", in_file)
                        continue

                    PSFile(
                        ps_path=in_file.as_posix(),
                        tb_name=item.shop_name,
                        ad_pic_list=[],
                    ).run_导出图片添加广告()
            pythoncom.CoUninitialize()  # type: ignore

        case "PSD-图层改名-导出图片-添加广告":
            # 获取所有PSD
            all_file = []
            all_file.extend(
                fun_遍历指定文件(material_structure.material_path, [".psd", ".psb"])
            )

            pythoncom.CoInitialize()  # type: ignore
            for in_file in tqdm(all_file, ncols=100, desc="导出图片，添加广告\t"):
                png_path = in_file.with_suffix(".png")
                if png_path.exists() is False:
                    if in_file.stat().st_size == 4096:
                        print("错误PSD文件", in_file)
                        continue
                    PSFile(
                        ps_path=in_file.as_posix(),
                        tb_name=item.shop_name,
                        ad_pic_list=[],
                    ).run_图层改名_导出图片()
            pythoncom.CoUninitialize()  # type: ignore

        case "PSD-导出图片":
            # 获取所有PSD
            all_file = []
            all_file.extend(
                fun_遍历指定文件(material_structure.material_path, [".psd", ".psb"])
            )

            pythoncom.CoInitialize()  # type: ignore
            for in_file in all_file:
                png_path = in_file.with_suffix(".png")
                if png_path.exists() is False:
                    if in_file.stat().st_size == 4096:
                        print("错误PSD文件", in_file)
                        continue
                    PSFile(
                        ps_path=in_file.as_posix(),
                        tb_name=item.shop_name,
                        ad_pic_list=[],
                    ).run_导出图片()
            pythoncom.CoUninitialize()  # type: ignore

        case "删除EPS文件":
            fun_删除EPS文件(material_path=material_structure.material_path)

        case "PPT-导出图片":
            all_file = []
            all_file.extend(
                fun_遍历指定文件(material_structure.material_path, [".ppt", ".pptx"])
            )

            for in_file in tqdm(all_file, ncols=100, desc="PPT导出图片"):
                png_path = in_file.with_suffix(".png")
                if png_path.exists() is False:
                    export_path = in_file.parent
                    PPTEdit(ppt_path=in_file, ppt_export_path=export_path).main()

        case "子目录内文件移动到根":
            for in_path in Path(material_structure.material_path).iterdir():
                fun_移动到根目录(in_path.as_posix())

        case "子目录重命名":
            fun_文件夹内文件夹重命名(
                material_path=material_structure.material_path,
                shop_name=item.shop_name,
                num=int(item.path_start_stem),
            )

        case "图片添加白色背景":
            fun_图片添加白色背景(material_path_text=material_structure.material_path)

        case "删除ZIP文件":
            for in_file in tqdm(
                fun_遍历指定文件(material_structure.material_path, [".zip", ".rar"]),
                ncols=100,
                desc="删除ZIP文件",
            ):
                print(in_file.as_posix())
                in_file.unlink()

        case "AI文件重命名":
            fun_ai文件重命名(material_path=material_structure.material_path)

        case "删除AI对应的PNG文件":
            fun_删除AI对应的PNG文件(material_path=material_structure.material_path)

        case "享设计制作预览图":
            fun_享设计制作预览图(
                material_path=material_structure.material_path, shop_name=item.shop_name
            )

        case "享设计文件夹重构":
            fun_享设计文件夹重构(material_path=material_structure.material_path)

        case "删除图片边框":
            fun_删除图片边框(material_path=material_structure.material_path)

        case "子目录PSD重命名":
            fun_子目录PSD重命名(material_path=material_structure.material_path)

        case "子目录图片重命名":
            fun_子目录图片重命名(material_path=material_structure.material_path)

    fun_通知(
        msg=f"素材ID:{Path(material_structure.material_path).name}\n{item.action}完成。"
    )

    return dict(msg="ok")
